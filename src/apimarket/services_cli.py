"""CLI generada a partir del registro de servicios.

Uso: ``apimarket <grupo> <servicio> [--parametro valor ...]``
"""
import argparse
import difflib
import functools
import json
import sys
import typing
from pathlib import Path

import httpx
from kiota_abstractions.api_error import APIError

import apimarket
from apimarket import cli_help
from apimarket.services import REGISTRY
from apimarket.services._core import FileInput
from apimarket.errors import ErrorCode, annotate
from apimarket.validations import ValidationError

LIST_COMMAND = "servicios"
ERRORS_COMMAND = "errores"
GROUPS = tuple(sorted({spec.group for spec in REGISTRY}))

def handles(args) -> bool:
    """Indica si los argumentos pertenecen a esta CLI y no a las opciones clásicas."""
    return bool(args) and args[0] in GROUPS + (LIST_COMMAND, ERRORS_COMMAND)


def _unwrap(annotation):
    """Quita ``Optional`` de una anotación."""
    if annotation == FileInput or annotation == typing.Optional[FileInput]:
        return FileInput
    arguments = [a for a in typing.get_args(annotation) if a is not type(None)]
    if typing.get_origin(annotation) is typing.Union and len(arguments) == 1:
        return arguments[0]
    return annotation


def _json_value(kind):
    """Lee un parámetro JSON escrito en la línea de comandos o en ``@archivo``."""

    def parse(text: str):
        try:
            raw = Path(text[1:]).read_text(encoding="utf-8") if text.startswith("@") else text
            value = json.loads(raw)
        except (OSError, ValueError) as error:
            raise argparse.ArgumentTypeError(f"JSON inválido: {error}")
        if not isinstance(value, kind):
            expected = "un arreglo" if kind is list else "un objeto"
            raise argparse.ArgumentTypeError(f"se esperaba {expected} JSON")
        return value

    return parse


def _add_parameter(parser, name, parameter, help_text):
    flag = cli_help.flag_name(name)
    annotation = _unwrap(parameter.annotation)
    is_required = parameter.default is parameter.empty
    options = {"dest": name, "help": help_text or None}

    if annotation is bool:
        if parameter.default:
            parser.add_argument("--no-" + flag[2:], action="store_false", **options)
        else:
            parser.add_argument(flag, action="store_true", **options)
        return

    options["required"] = is_required
    options["default"] = argparse.SUPPRESS
    origin = typing.get_origin(annotation)
    if annotation == FileInput:
        options.update(metavar="ARCHIVO")
    elif annotation is int:
        options.update(type=int, metavar="N")
    elif origin is list and typing.get_args(annotation) == (str,):
        options.update(type=lambda text: [item.strip() for item in text.split(",") if item.strip()],
                       metavar="A,B")
    elif origin in (list, dict):
        options.update(type=_json_value(origin), metavar="JSON|@ARCHIVO")
    else:
        options.update(metavar=name.upper())
    parser.add_argument(flag, **options)


def build_parser() -> argparse.ArgumentParser:
    parser = Parser(prog="apimarket")
    groups = parser.add_subparsers(dest="group", metavar="ÁREA", required=True, parser_class=Parser)
    groups.add_parser(LIST_COMMAND, renderer=cli_help.services_list)
    errors = groups.add_parser(ERRORS_COMMAND)
    errors.add_argument("text", metavar="TEXTO", nargs="?", default="")

    for group in GROUPS:
        group_parser = groups.add_parser(group, renderer=functools.partial(cli_help.group_help, group))
        commands = group_parser.add_subparsers(dest="command", metavar="SERVICIO", required=True,
                                               parser_class=Parser)
        for spec in (s for s in REGISTRY if s.group == group):
            command = commands.add_parser(spec.command, allow_abbrev=False,
                                          renderer=functools.partial(cli_help.command_help, spec))
            for name, parameter in spec.signature.parameters.items():
                _add_parameter(command, name, parameter, None)
            command.add_argument("--sandbox", dest="_sandbox", action="store_true")
            command.set_defaults(_spec=spec)
    return parser


def main(args):
    # "apimarket sat" muestra la ayuda del área.
    if len(args) == 1 and args[0] in GROUPS:
        print(cli_help.group_help(args[0]), end="")
        return
    namespace = vars(build_parser().parse_args(args))
    if namespace["group"] == LIST_COMMAND:
        print(cli_help.services_list())
        return
    if namespace["group"] == ERRORS_COMMAND:
        print(cli_help.error_catalog(namespace["text"]), end="")
        return

    spec = namespace["_spec"]
    kwargs = {name: namespace[name] for name in spec.signature.parameters if name in namespace}
    if namespace["_sandbox"]:
        apimarket.assemble(sandbox=True, headers={"x-sandbox": "true"})

    try:
        result = spec.function(**kwargs)
    except HANDLED_ERRORS as error:
        report_error(error)

    if isinstance(result, bytes):
        sys.stdout.buffer.write(result)
    else:
        print(apimarket.to_json(result))


#: Errores que la CLI muestra como ``Error [CÓDIGO]: mensaje``.
HANDLED_ERRORS = (ValidationError, APIError, httpx.HTTPError)


def report_error(error: Exception):
    """Imprime el error con su código y sale con código 1."""
    if isinstance(error, ValidationError):
        _fail(error.code, error.message)
    annotate(error)
    if isinstance(error, APIError):
        body = getattr(error, "body", None)
        if isinstance(body, (dict, list)):
            print(json.dumps(body, ensure_ascii=False))
        elif hasattr(error, "serialize"):  # errores tipados por endpoint
            print(apimarket.to_json(error))
        # En los errores tipados str(error) solo muestra el nombre de la clase; el mensaje está en .message.
        status = f" (status {error.response_status_code})" if error.response_status_code else ""
        _fail(error.code, f"{error.message or 'La API respondió con un error.'}{status}")
    _fail(error.code, error.message)


def _fail(code, message: str, status: int = 1):
    print(f"Error [{code.value}]: {message}", file=sys.stderr)
    sys.exit(status)


def usage_error(message: str):
    _fail(ErrorCode.CLI_ARGUMENTS_INVALID, message, status=2)


def unknown_area(name: str):
    """Error para una primera palabra que no es un área ni una opción."""
    close = difflib.get_close_matches(name, GROUPS + (LIST_COMMAND, ERRORS_COMMAND), 2)
    hint = f" ¿Quiso decir: {', '.join(close)}?" if close else ""
    print("Ejecute 'apimarket --help' para ver las opciones.", file=sys.stderr)
    usage_error(f"'{name}' no es un área ni una opción.{hint}")


class Parser(argparse.ArgumentParser):
    """Muestra la ayuda de :mod:`apimarket.cli_help` y los errores de uso con su código."""

    def __init__(self, *args, renderer=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.renderer = renderer

    def format_help(self):
        return self.renderer() if self.renderer else super().format_help()

    def error(self, message):
        print(f"Ejecute '{self.prog} --help' para ver las opciones.", file=sys.stderr)
        usage_error(cli_help.translate(message))
