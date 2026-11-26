"""Presentación de la ayuda de la CLI.

Los comandos, sus parámetros y sus códigos se leen del registro de servicios y del
catálogo de errores; aquí solo viven los textos y el formato.
"""
import argparse
import difflib
import inspect
import os
import re
import shutil
import sys
import textwrap

from apimarket.errors import CATALOG
from apimarket.services import REGISTRY
from apimarket.validations import (InvalidCreditError, InvalidCURPError, InvalidFileError, InvalidNSSError,
                                   InvalidParameterError, InvalidRFCError, code_token)

#: Áreas en el orden en que se muestran: clave, título y grupo de las opciones cortas.
AREAS = (
    ("cuenta", "Cuenta", "Cuenta"),
    ("renapo", "RENAPO", "RENAPO"),
    ("sat", "SAT", "SAT"),
    ("imss", "IMSS e IDSE", "IMSS"),
    ("idse", "IDSE Pro", "IDSE Pro"),
    ("infonavit", "INFONAVIT", "INFONAVIT"),
    ("sep", "SEP", "SEP"),
    ("repuve", "REPUVE", None),
    ("ai", "Inteligencia artificial", None),
    ("geo", "Geolocalización", None),
)
TITLES = {key: title for key, title, _ in AREAS}

_UUID = "550e8400-e29b-41d4-a716-446655440000"

#: Nombre del parámetro: (descripción, valor de ejemplo).
PARAMETERS = {
    "anverso": ("Imagen o PDF del frente de la identificación", "frente.jpg"),
    "blob_path": ("URL del documento que devolvió la búsqueda", "https://example.com/cfdi"),
    "certificate": ("Certificado .cer de la e.firma", "certificado.cer"),
    "ciec": ("Contraseña CIEC; si se omite se usa la guardada en el token", "MiCiec123"),
    "codigo_postal": ("Código postal fiscal, 5 dígitos", "01000"),
    "codigo_validacion_relacionado": ("Código de validación de la captura, 20 caracteres", "AbCdEfGhIjKlMnOpQrSt"),
    "company": ("Empresa del token", "Mi Empresa"),
    "complementos": ("Complementos separados por comas", "pago"),
    "correo": ("Correo electrónico", "persona@example.com"),
    "country_code": ("Filtro de país con operador", "eq.MX"),
    "credentials": ("JSON con userId, password, certificate y privateKey", "@credenciales.json"),
    "csf": ("Constancia de Situación Fiscal en PDF o imagen", "constancia.pdf"),
    "curp": ("CURP de 18 caracteres, en mayúsculas", "XEXX010101MNEXXXA4"),
    "data": ("Archivo CSV", "datos.csv"),
    "dataset": ("Nombre del dataset", "clientes"),
    "delay": ("Fecha en que debe procesarse, AAAA-MM-DD", "2030-01-31"),
    "description": ("Descripción del token", "Integración"),
    "email": ("Correo que recibe el resultado", "persona@example.com"),
    "estado_comprobante": ("Estado del comprobante", "1"),
    "fecha_final": ("Fin del periodo, AAAA-MM-DD", "2024-01-31"),
    "fecha_inicial": ("Inicio del periodo, AAAA-MM-DD", "2024-01-01"),
    "filter": ("Filtro en JSON", '{"estado":"activo"}'),
    "formato": ("xml, pdf o ambos", "pdf"),
    "idcif": ("idCIF de la constancia, solo dígitos", "12345678901"),
    "identificador": ("NSS, RFC o CURP; en INFONAVIT también número de crédito", "XEXX010101MNEXXXA4"),
    "inputs": ("JSON: arreglo de 1 a 100 objetos con los valores", "@valores.json"),
    "lote": ("Número de lote de la captura", "1"),
    "movimientos": ("JSON: arreglo de movimientos afiliatorios", "@movimientos.json"),
    "name": ("Nombre del token", "Produccion"),
    "nombre": ("Nombre o razón social", "PUBLICO EN GENERAL"),
    "nss": ("Número de Seguridad Social, 11 dígitos", "12345678903"),
    "num_credito": ("Número de crédito INFONAVIT, 10 dígitos", "1234567890"),
    "numero_serie": ("Número de serie (NIV), hasta 50 caracteres", "3VW000000000000"),
    "options": ("JSON: filename, title, correlation_id o metadata", "@opciones.json"),
    "page": ("Página, desde 1", "1"),
    "page_size": ("Resultados por página, de 1 a 10000", "100"),
    "password": ("Contraseña de la e.firma", "MiClave"),
    "per_page": ("Filas por página, de 1 a 100", "25"),
    "periodicidad": ("M (mensual) o Y (del ejercicio)", "M"),
    "periodo": ("Mes de 1 a 12 si es M; 0 o 043 si es Y", "3"),
    "permissions": ("Permisos separados por comas", "use_valida_curp"),
    "placas": ("Placas, hasta 10 caracteres", "ABC1234"),
    "postal_code": ("Filtro de código postal con operador", "eq.10001"),
    "postal_code_mx": ("Código postal mexicano, 5 dígitos", "01000"),
    "privateKey": ("Llave privada .key de la e.firma", "llave.key"),
    "regimen_fiscal": ("Régimen fiscal, 3 dígitos", "616"),
    "reset": ("Ignora la caché y consulta de nuevo", ""),
    "resource": ("Nombre del dataset", "clientes"),
    "resources": ("JSON: arreglo con resource, field, url y json_path_query", "@recursos.json"),
    "reverso": ("Imagen o PDF del reverso", "reverso.jpg"),
    "rfc": ("RFC en mayúsculas", "XAXX010101000"),
    "rfc_emisor": ("RFC del emisor", "XAXX010101000"),
    "rfc_receptor": ("RFC del receptor", "XAXX010101000"),
    "rfc_tercero": ("RFC del tercero", "XAXX010101000"),
    "row_id": ("Identificador de la fila", "1"),
    "select": ("Columnas separadas por comas", "postal_code,place_name"),
    "sort": ("Columna de orden; con - es descendente", "-id"),
    "template": ("Plantilla PDFMe en JSON", "plantilla.json"),
    "template_id": ("Identificador de la plantilla", "1"),
    "tipo_comprobante": ("I, E, T, N o P", "I"),
    "transaction_id": ("Número de transacción", "1"),
    "uso_cfdi": ("Uso del CFDI", "S01"),
    "uuid": ("UUID del documento o mensaje", _UUID),
    "wait": ("No esperar a que termine la generación", ""),
    "webhook": ("URL https que recibe el resultado", "https://example.com/webhook"),
    "year": ("Ejercicio, 4 dígitos", "2024"),
}

#: Opcionales que el ejemplo necesita para ser una consulta válida.
_EXAMPLE_EXTRAS = {
    "get_vehicle_owner": ("placas",), "get_vehicle_data": ("placas",), "check_vehicle_theft": ("placas",),
    "search_postal_codes": ("postal_code_mx",), "store_token": ("permissions",),
}

#: Contenido de los parámetros que reciben JSON.
JSON_SAMPLES = {
    "credentials": '{"userId": "...", "password": "...", "certificate": "...", "privateKey": "..."}',
    "movimientos": '[{"nss": "12345678903", "nombre": "JUAN", "apellidoPaterno": "PEREZ",\n'
                   '  "tipoDeMovimiento": "2", "causaDeBaja": "1", "fechaDeMovimiento": "31-01-2024",\n'
                   '  "registroPatronal": "A1234567890"}]\n'
                   'tipoDeMovimiento: 2 baja, 7 modificación, 8 reingreso. Con 7 u 8 agregue\n'
                   'salarioDiarioIntegrado, tipoDeSalario y jornada; con 8, umf y tipoDeTrabajador.',
    "inputs": '[{"nombre": "valor"}]',
    "options": '{"filename": "documento.pdf", "title": "Contrato"}',
    "resources": '[{"resource": "clientes", "field": "curp", "url": "https://...", "json_path_query": "$.data"}]',
    "filter": '{"estado": "activo", "nombre": {"like": "juan"}}',
}

_DOMAIN_CODES = {"curp": InvalidCURPError, "rfc": InvalidRFCError, "rfc_emisor": InvalidRFCError,
                 "rfc_receptor": InvalidRFCError, "rfc_tercero": InvalidRFCError, "nss": InvalidNSSError,
                 "num_credito": InvalidCreditError}


# ---------------------------------------------------------------------------
# Formato
# ---------------------------------------------------------------------------

def _color_enabled() -> bool:
    return sys.stdout.isatty() and "NO_COLOR" not in os.environ and os.environ.get("TERM") != "dumb"


def _paint(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if _color_enabled() else text


def bold(text):
    return _paint("1", text)


def dim(text):
    return _paint("2", text)


def accent(text):
    return _paint("36", text)


def warn(text):
    return _paint("33", text)


def width() -> int:
    return max(72, min(shutil.get_terminal_size((96, 24)).columns, 110))


def title(text: str) -> str:
    return bold(accent(text.upper()))


def paragraph(text: str, indent: int = 2, style=None, hanging: int = 0) -> list:
    """Texto ajustado al ancho de la terminal."""
    lines = textwrap.wrap(text, width(), initial_indent=" " * indent, subsequent_indent=" " * (indent + hanging),
                          break_on_hyphens=False, break_long_words=False)
    return [style(line) for line in lines] if style else lines


def command_lines(parts: list) -> list:
    """Comando en varios renglones con ``\\``, listo para copiar y pegar."""
    lines, current = [], "  " + parts[0]
    for part in parts[1:]:
        # Un valor no se separa de su opción.
        if len(current) + len(part) + 3 > width() and not current.isspace():
            lines.append(current + " \\")
            current = "      " + part
        else:
            current += " " + part
    return lines + [current]


def section(text: str, note: str = "") -> str:
    rule = "─" * max(3, width() - len(text) - len(note) - (4 if not note else 5))
    extra = f" {dim(note)}" if note else ""
    return f"\n{title(text)}{extra} {dim(rule)}"


def rows(items, column: int = 30, indent: int = 2):
    """Dos columnas. Si la primera no cabe, la descripción pasa al renglón siguiente."""
    lines = []
    space = max(24, width() - indent - column - 2)
    for left, description, *tags in items:
        wrapped = textwrap.wrap(description, space) or [""]
        suffix = "".join(f" {warn('[' + tag + ']')}" for tag in tags if tag)
        if suffix:
            visible = sum(len(tag) + 3 for tag in tags if tag)
            if len(wrapped[-1]) + visible > space:
                wrapped.append("")
                suffix = suffix.lstrip()
        wrapped[-1] += suffix
        if len(left) > column:
            pieces = textwrap.wrap(left, width() - indent - 4, break_on_hyphens=False, break_long_words=False)
            lines += [" " * (indent + 4 * bool(n)) + accent(piece) for n, piece in enumerate(pieces[:-1])]
            lines.append(" " * (indent + 4 * (len(pieces) > 1)) + accent(pieces[-1]))
            first = " " * (indent + column + 2) + wrapped[0]
        else:
            first = " " * indent + accent(left) + " " * (column - len(left) + 2) + wrapped[0]
        lines.append(first)
        lines += [" " * (indent + column + 2) + line for line in wrapped[1:]]
    return lines


def _header(subtitle: str, version: str = "") -> list:
    name = f"{bold('API Market')} {dim('·')} "
    version = f"v{version.split('+')[0]}" if version else ""
    if len(f"API Market · {subtitle}  {version}") <= width():
        return ["", name + subtitle + (dim("  " + version) if version else "")]
    return ["", name + (dim(version) if version else ""), *paragraph(subtitle, 0)]


def flag_name(parameter: str) -> str:
    return "--" + parameter.replace("_", "-").replace("privateKey", "private-key")


def _tags(spec):
    return ("modifica" if not spec.retry else "",)


def parameter_help(spec) -> dict:
    """Descripción de cada parámetro: la del docstring o, si no hay, la general."""
    documented = dict(re.findall(r":param (\w+):\s*(.*?)(?=\n:param |\Z)",
                                 inspect.cleandoc(spec.function.__doc__ or ""), re.S))
    result = {}
    for name in spec.signature.parameters:
        text = " ".join(documented.get(name, PARAMETERS[name][0]).split())
        text = text.replace("``", "").rstrip(".")
        result[name] = text[:1].upper() + text[1:] if not text.startswith("userId") else text
    return result


def example_arguments(spec) -> list:
    """Argumentos del ejemplo que se muestra en la ayuda de cada comando."""
    extras = _EXAMPLE_EXTRAS.get(spec.function.__name__, ())
    arguments = []
    for name, parameter in spec.signature.parameters.items():
        if parameter.default is parameter.empty or name in extras:
            arguments += [flag_name(name), PARAMETERS[name][1]]
    return arguments


def _quote(value: str) -> str:
    return f"'{value}'" if re.search(r"[\s{}\"|&;<>*?$]", value) else value


def _value_label(name: str, parameter) -> str:
    if isinstance(parameter.default, bool):
        return ("--no-" + flag_name(name)[2:]) if parameter.default else flag_name(name)
    annotation = str(parameter.annotation)
    if name in ("anverso", "reverso", "template", "data", "csf", "certificate", "privateKey"):
        kind = "ARCHIVO"
    elif name in ("credentials", "movimientos", "inputs", "options", "resources", "filter"):
        kind = "JSON"
    elif name in ("permissions", "complementos"):
        kind = "A,B"
    elif "int" in annotation:
        kind = "N"
    else:
        kind = name.upper()
    return f"{flag_name(name)} {kind}"


def parameter_codes(name: str) -> list:
    """Códigos de validación que puede producir un parámetro."""
    token = code_token(name)
    codes = [code.value for code in _DOMAIN_CODES[name].Code] if name in _DOMAIN_CODES else []
    codes += [c.value for c in InvalidParameterError.Code if c.name.rsplit("_", 1)[0] == token]
    codes += [c.value for c in InvalidFileError.Code if c.name.split("_FILE_")[0] == token]
    return codes


# ---------------------------------------------------------------------------
# Pantallas
# ---------------------------------------------------------------------------

def _short_options(parser) -> dict:
    """Opciones cortas visibles, agrupadas como en el analizador."""
    groups = {}
    for group in parser._action_groups:
        for action in group._group_actions:
            if action.help == argparse.SUPPRESS or not action.option_strings:
                continue
            metavar = action.metavar or ""
            if isinstance(metavar, tuple):
                metavar = " ".join(metavar)
            label = f"{', '.join(action.option_strings)} {metavar}".strip()
            description = (action.help or "").split("\n")[0].rstrip(".")
            groups.setdefault(group.title, []).append((label, description, ""))
    return groups


def main_help(parser, version: str) -> str:
    short = _short_options(parser)
    out = _header("servicios gubernamentales de México desde la terminal", version)
    out += [section("Uso"), *rows([
        ("apimarket ÁREA SERVICIO", "Servicios con parámetros por nombre: --curp, --rfc, ..."),
        ("apimarket -XX VALOR ...", "Opciones cortas, con los valores en orden"),
    ])]
    out += [section("Empezar"), *rows([
        ("apimarket cuenta saldo", "Comprueba que su llave funciona"),
        ("apimarket sat -h", "Ayuda de un área"),
        ("apimarket sat declaraciones -h", "Parámetros, ejemplo y errores de un servicio"),
    ], column=32)]

    for key, heading, short_group in AREAS:
        items = [(label, text, "") for label, text, _ in short.get(short_group, [])]
        services = [(f"{s.group} {s.command}", s.summary.rstrip("."), *_tags(s))
                    for s in sorted(REGISTRY, key=lambda s: s.command) if s.group == key]
        if not items and not services:
            continue
        out.append(section(heading))
        out += rows(items)
        if items and services:
            out.append("")
        out += rows(services)

    out += [section("Opciones generales"), *rows([
        ("-h, --help", "Muestra esta ayuda"),
        ("--version", "Muestra la versión"),
        ("--sandbox", "Modo de pruebas en ÁREA SERVICIO; no aplica a todos"),
        ("-v, -vv", "Más detalle en los registros"),
        ("servicios", "Lista los servicios por área"),
        ("errores [TEXTO]", "Catálogo de códigos de error; TEXTO filtra"),
    ])]
    out += [section("Configuración"), dim("  Variables de entorno o archivo .env"), *rows([
        ("APIMARKET_API_KEY", "Llave de https://apimarket.mx/app/tokens"),
        ("APIMARKET_SANDBOX", "true activa el modo de pruebas en todos los comandos"),
        ("IDSEPRO_BEARER_TOKEN", "Solo para IDSE Pro, junto con IDSEPRO_API_KEY"),
    ])]
    out += [section("Salida y errores"), *rows([
        ("Respuesta", "JSON en la salida estándar"),
        ("Error", "Error [CÓDIGO]: mensaje, en la salida de errores"),
        ("Código de salida", "0 correcto, 1 error, 2 argumentos incorrectos"),
    ])]
    out += ["", *rows([("[modifica]", "Crea, cambia o marca datos; no confíe en --sandbox")], column=15), ""]
    return "\n".join(out) + "\n"


def group_help(group: str) -> str:
    services = [s for s in sorted(REGISTRY, key=lambda s: s.command) if s.group == group]
    out = _header(TITLES[group])
    out += [section("Uso"), f"  apimarket {group} SERVICIO [--parametro valor ...]", section("Servicios")]
    for spec in services:
        required = [flag_name(n) for n, p in spec.signature.parameters.items() if p.default is p.empty]
        out += rows([(spec.command, spec.summary.rstrip("."), *_tags(spec))])
        if required:
            out += paragraph("requiere " + " ".join(required), 34, dim, hanging=2)
    out += ["", *paragraph(f"Detalle: apimarket {group} SERVICIO -h", style=dim), ""]
    return "\n".join(out) + "\n"


def command_help(spec) -> str:
    helps = parameter_help(spec)
    name = f"apimarket {spec.group} {spec.command}"
    parameters = spec.signature.parameters
    required = {n: p for n, p in parameters.items() if p.default is p.empty}
    optional = {n: p for n, p in parameters.items() if n not in required}

    out = _header(f"{TITLES[spec.group]} › {spec.command}")
    out += ["", *paragraph(spec.summary)]
    if not spec.retry:
        out += paragraph("Crea, cambia o marca datos: no confíe en --sandbox.", style=warn)

    usage = [name, *[_value_label(n, p) for n, p in required.items()], "[opciones]"]
    out += [section("Uso"), *textwrap.wrap(" ".join(usage), width() - 2, initial_indent="  ",
                                          subsequent_indent="      ", break_on_hyphens=False,
                                          break_long_words=False)]
    if required:
        out += [section("Obligatorios"),
                *rows([(_value_label(n, p), helps[n], "") for n, p in required.items()], column=34)]
    out += [section("Opcionales"),
            *rows([(_value_label(n, p), helps[n], "") for n, p in optional.items()]
                  + [("--sandbox", "Modo de pruebas; no disponible en todos los servicios", ""),
                     ("-h, --help", "Muestra esta ayuda", "")], column=34)]

    example = example_arguments(spec)
    pairs, flags = [], iter(_quote(part) for part in example)
    for part in flags:
        pairs.append(f"{part} {next(flags)}")
    out += [section("Ejemplo"), *command_lines([name, *pairs])]

    samples = [n for n in parameters if n in JSON_SAMPLES]
    if samples:
        out.append(section("Formato JSON", "escrito directo o en un archivo con @nombre.json"))
        for parameter in samples:
            out.append("  " + accent(flag_name(parameter)))
            for line in JSON_SAMPLES[parameter].split("\n"):
                out += textwrap.wrap(line, width() - 4, initial_indent="    ", subsequent_indent="      ")

    with_codes = [(n, parameter_codes(n)) for n in parameters]
    with_codes = [(n, codes) for n, codes in with_codes if codes]
    if with_codes:
        out.append(section("Errores de validación"))
        for parameter, codes in with_codes:
            out.append("  " + accent(flag_name(parameter)))
            out += textwrap.wrap(", ".join(codes), width() - 4, initial_indent="    ", subsequent_indent="    ",
                                 break_on_hyphens=False, break_long_words=False)
            if parameter in ("movimientos", "credentials", "options", "resources"):
                out += paragraph(f"Los de cada campo: apimarket errores INVALID_{code_token(parameter)}_", 4, dim)
    out += ["", *paragraph("Errores de la API y de red: apimarket errores API · apimarket errores NETWORK",
                           style=dim, hanging=2), ""]
    return "\n".join(out) + "\n"


def services_list() -> str:
    out = _header(f"{len(REGISTRY)} servicios por área")
    for key, heading, _ in AREAS:
        services = [(f"{s.group} {s.command}", s.summary.rstrip("."), *_tags(s))
                    for s in sorted(REGISTRY, key=lambda s: s.command) if s.group == key]
        if services:
            out += [section(f"{heading} ({len(services)})"), *rows(services)]
    out += ["", *paragraph("Detalle: apimarket ÁREA SERVICIO -h", style=dim), ""]
    return "\n".join(out)


def error_catalog(text: str = "") -> str:
    """Catálogo completo o los códigos cuyo nombre o categoría contienen ``text``."""
    wanted = text.strip().upper()
    blocks, total = [], 0
    for heading, exception, codes in CATALOG:
        selected = [(c, d) for c, d in codes if wanted in c.value or wanted in heading.upper()]
        if selected:
            total += len(selected)
            blocks.append(section(heading, exception))
            blocks += rows([(c.value, d, "") for c, d in selected], column=44)
    if not blocks:
        return f"\nSin códigos que contengan '{text}'.\n"
    count = f"{total} código{'s' if total != 1 else ''}"
    out = _header(f"catálogo de errores: {count}")
    out += ["", *paragraph("INVALID_<CAMPO>_<MOTIVO> en datos; API_, NETWORK_, CONFIG_ y CLI_ según el origen",
                           style=dim), *blocks]
    if not wanted:
        out += ["", *paragraph("Filtre con: apimarket errores TEXTO (por ejemplo: curp, year, API)", style=dim)]
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# Mensajes de argparse en español
# ---------------------------------------------------------------------------

_MESSAGES = (
    (r"the following arguments are required: (.*)", r"Faltan argumentos obligatorios: \1"),
    (r"argument (\S+): expected one argument", r"El argumento \1 necesita un valor."),
    (r"argument (\S+): expected (\d+) arguments", r"El argumento \1 necesita \2 valores."),
    (r"argument (\S+): expected at least one argument", r"El argumento \1 necesita al menos un valor."),
    (r"unrecognized arguments: (.*)", r"Argumentos no reconocidos: \1"),
    (r"argument (\S+): invalid int value: (.*)", r"El argumento \1 debe ser un número entero, no \2."),
    (r"ambiguous option: (\S+) could match (.*)", r"La opción \1 es ambigua; puede ser: \2"),
    (r"argument (\S+): (.*)", r"Argumento \1: \2"),
)


def _unknown_choice(match) -> str:
    argument, value, choices = match.groups()
    options = [option.strip(" '") for option in choices.split(",")]
    kind = {"ÁREA": "un área", "SERVICIO": "un servicio"}.get(argument, f"una opción de {argument}")
    close = difflib.get_close_matches(value.strip("'"), options, 3)
    hint = f" ¿Quiso decir: {', '.join(close)}?" if close else ""
    return f"{value} no es {kind}.{hint}"


def translate(message: str) -> str:
    choice = re.fullmatch(r"argument (\S+): invalid choice: (.*?) \(choose from (.*)\)", message, re.S)
    if choice:
        return _unknown_choice(choice)
    for pattern, replacement in _MESSAGES:
        if re.fullmatch(pattern, message, re.S):
            return re.sub(pattern, replacement, message, flags=re.S)
    return message
