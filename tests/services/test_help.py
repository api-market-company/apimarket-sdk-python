"""La ayuda de la CLI está completa, cabe en la terminal y sus ejemplos funcionan."""
import json

import pytest

from apimarket import cli_help
from apimarket.cli import main
from apimarket.services import REGISTRY

from cases import CSV, MOVEMENT, PDF, RESOURCE, TEMPLATE

IDS = [f"{spec.group} {spec.command}" for spec in REGISTRY]
CREDENTIALS = {"userId": "u", "password": "p", "certificate": "c", "privateKey": "k"}
FILES = {
    "constancia.pdf": PDF, "frente.jpg": b"\xff\xd8\xff\xe0", "reverso.jpg": b"\xff\xd8\xff\xe0",
    "certificado.cer": b"certificado", "llave.key": b"llave", "plantilla.json": TEMPLATE, "datos.csv": CSV,
    "credenciales.json": json.dumps(CREDENTIALS).encode(), "movimientos.json": json.dumps([MOVEMENT]).encode(),
    "valores.json": b'[{"nombre": "valor"}]', "opciones.json": b'{"title": "t"}',
    "recursos.json": json.dumps([RESOURCE]).encode(),
}


def screen(capsys, *argv):
    try:
        main(list(argv))
    except SystemExit as exit_:
        assert exit_.code == 0
    return capsys.readouterr().out


@pytest.mark.parametrize("argv", [["-h"], ["--help"], []])
def test_main_help_lists_every_command(capsys, argv):
    output = screen(capsys, *argv)
    missing = [name for name in IDS if f"  {name} " not in output]
    assert missing == []
    for option in ("-bn", "-vc", "-cc", "-ro", "-cr", "-vs", "-df", "-l69", "-lu", "-ln", "-vi", "-cl", "-hl",
                   "-ce", "-vr", "-oc", "-bc", "-si", "-lc", "-pm", "-gt", "servicios", "errores", "--sandbox",
                   "APIMARKET_API_KEY"):
        assert option in output
    assert "\033[" not in output  # sin colores cuando la salida no es una terminal


@pytest.mark.parametrize("group", sorted({spec.group for spec in REGISTRY}))
def test_area_help(capsys, group):
    output = screen(capsys, group)
    assert output == screen(capsys, group, "-h")
    assert all(f"  {spec.command} " in output for spec in REGISTRY if spec.group == group)


@pytest.mark.parametrize("spec", REGISTRY, ids=IDS)
def test_command_help_describes_every_parameter(capsys, spec):
    output = screen(capsys, spec.group, spec.command, "-h")
    for name, parameter in spec.signature.parameters.items():
        assert cli_help.PARAMETERS[name][0]
        assert cli_help.flag_name(name)[2:] in output
        for code in cli_help.parameter_codes(name):
            assert code in output
    assert "EJEMPLO" in output


@pytest.mark.parametrize("spec", REGISTRY, ids=IDS)
def test_command_example_works(server, tmp_path, monkeypatch, capsys, spec):
    monkeypatch.chdir(tmp_path)
    for name, content in FILES.items():
        (tmp_path / name).write_bytes(content)
    main([spec.group, spec.command, *cli_help.example_arguments(spec)])
    assert len(server.requests) == 1


@pytest.mark.parametrize("columns", [72, 100])
def test_help_fits_the_terminal(capsys, monkeypatch, columns):
    monkeypatch.setenv("COLUMNS", str(columns))
    screens = [["-h"], ["servicios"], ["errores"]]
    screens += [[group] for group in {spec.group for spec in REGISTRY}]
    screens += [[spec.group, spec.command, "-h"] for spec in REGISTRY]
    for argv in screens:
        assert [line for line in screen(capsys, *argv).splitlines() if len(line) > columns] == [], argv


def test_errors_can_be_filtered(capsys):
    output = screen(capsys, "errores", "curp")
    assert "INVALID_CURP_DIGIT" in output and "INVALID_RFC_FORMAT" not in output
    assert "Sin códigos" in screen(capsys, "errores", "no-existe")


@pytest.mark.parametrize("argv, message", [
    (["infonabit"], "¿Quiso decir: infonavit?"),
    (["sat", "declaracion"], "¿Quiso decir: declaraciones"),
    (["sat", "declaraciones"], "Faltan argumentos obligatorios: --year"),
    (["sat", "declaraciones", "--year", "dos"], "El argumento --year debe ser un número entero"),
    (["-vi", "1"], "necesita 2 valores"),
    (["cuenta", "saldo", "--otro"], "Argumentos no reconocidos: --otro"),
])
def test_usage_errors_are_in_spanish(server, capsys, argv, message):
    with pytest.raises(SystemExit) as exit_:
        main(argv)
    assert exit_.value.code == 2
    error = capsys.readouterr().err
    assert "Error [CLI_ARGUMENTS_INVALID]:" in error and message in error
    assert server.requests == []
