"""Comportamiento común a los servicios declarativos, contra un servidor local."""
import asyncio
import json
from concurrent.futures import ThreadPoolExecutor

import pytest
from kink import di
from kiota_abstractions.api_error import APIError

import apimarket
from apimarket import ApiMarketError
from apimarket.api_market_client import ApiMarketClient
from apimarket.cli import main
from apimarket.services import REGISTRY
from apimarket.validations import InvalidParameterError

from cases import CASES, CURP, MOVEMENT, NSS, RFC, WEBHOOK
from support import connect


def test_every_service_has_a_case():
    assert sorted(case[0] for case in CASES) == sorted(spec.function.__name__ for spec in REGISTRY)


def test_cli_commands_are_unique():
    commands = [(spec.group, spec.command) for spec in REGISTRY]
    assert len(commands) == len(set(commands))


@pytest.mark.parametrize("code", [400, 401, 403, 404, 422, 500])
def test_api_error_has_the_same_fields_as_typed_errors(server, code):
    payload = {"success": False, "codigoValidacion": "ABC123", "message": f"mensaje {code}", "status": code,
               "data": {"campo": ["detalle"]}, "extra": 1}
    server.reply = (code, "application/json", json.dumps(payload).encode())
    with pytest.raises(APIError) as exc_info:
        apimarket.get_assigned_umf(NSS)
    error = exc_info.value
    assert error.message == f"mensaje {code}"
    assert (error.status, error.response_status_code) == (code, code)
    assert error.success is False
    assert error.codigo_validacion == "ABC123"
    assert error.data == {"campo": ["detalle"]}
    assert error.additional_data == {"extra": 1}
    assert error.body == payload
    assert str(error) == f"mensaje {code} (status {code})"


def test_api_error_without_json_body(server):
    server.reply = (502, "text/html", b"<html></html>")
    with pytest.raises(ApiMarketError) as exc_info:
        apimarket.get_assigned_umf(NSS)
    error = exc_info.value
    assert error.response_status_code == 502
    assert (error.status, error.success, error.codigo_validacion, error.data) == (None, None, None, None)
    assert error.additional_data == {}


def test_parameter_error_keeps_value_error_compatibility():
    with pytest.raises(ValueError) as exc_info:
        apimarket.get_employment_trajectory("")
    error = exc_info.value
    assert error.parameter == "identificador"
    assert str(error) == "[INVALID_IDENTIFICADOR_MISSING] Parámetro: identificador - El parámetro 'identificador' es obligatorio."


def test_parameter_error_in_cli(server, capsys):
    with pytest.raises(SystemExit) as exit_:
        main(["repuve", "vehiculo"])
    assert exit_.value.code == 1
    assert "Error [INVALID_NUMERO_SERIE_PLACAS_MISSING]: Indique" in capsys.readouterr().err


def test_parameter_error_in_legacy_cli(server, capsys):
    with pytest.raises(SystemExit) as exit_:
        main(["-gt", "", "", "", "permiso", "", ""])
    assert exit_.value.code == 1
    assert "Error [INVALID_NAME_MISSING]:" in capsys.readouterr().err


def test_path_errors_are_raised_before_awaiting(server):
    connect(server, async_client=True)
    with pytest.raises(InvalidParameterError):
        apimarket.read_sat_message("..")
    assert server.requests == []


def test_error_response(server, capsys):
    server.reply = (401, "application/json", b'{"message":"Unauthenticated."}')
    with pytest.raises(ApiMarketError) as error:
        apimarket.get_balance()
    assert error.value.response_status_code == 401
    assert error.value.body == {"message": "Unauthenticated."}

    with pytest.raises(SystemExit) as exit_:
        main(["cuenta", "saldo"])
    assert exit_.value.code == 1
    assert "Error [API_KEY_UNAUTHORIZED]: Unauthenticated. (status 401)" in capsys.readouterr().err


def test_non_json_response(server):
    server.reply = (200, "application/pdf", b"%PDF-1.7")
    assert apimarket.get_sat_csf() == b"%PDF-1.7"


def test_mutations_are_not_retried(server):
    server.reply = (503, "application/json", b'{"message":"no disponible"}')
    with pytest.raises(ApiMarketError):
        apimarket.idse_capture_movements([MOVEMENT], WEBHOOK)
    assert len(server.requests) == 1


def test_queries_keep_default_retries(server):
    server.reply = (503, "application/json", b'{"message":"no disponible"}')
    with pytest.raises(ApiMarketError):
        apimarket.get_balance()
    assert len(server.requests) > 1


@pytest.mark.parametrize("content,filename", [
    (b"%PDF-1.7", "csf.pdf"),
    (b"\x89PNG\r\n\x1a\n", "csf.png"),
    (b"\xff\xd8\xff\xe0", "csf.jpg"),
])
def test_unnamed_files_get_an_extension_from_their_content(server, content, filename):
    apimarket.parse_csf(content)
    assert f'filename="{filename}"'.encode() in server.last["body"]


def test_named_files_keep_their_name(server, tmp_path):
    path = tmp_path / "constancia.PDF"
    path.write_bytes(b"%PDF-1.7")
    apimarket.parse_csf(path)
    assert b'filename="constancia.PDF"' in server.last["body"]


def test_path_parameters_are_escaped(server):
    apimarket.smart_processing_delete("a/../b?c")
    assert server.last["path"] == "/api/ai/v2/smart-processing/a%2F..%2Fb%3Fc"
    assert server.last["query"] == {}


def test_sandbox_and_reset_headers(server):
    connect(server, sandbox=True)
    apimarket.get_rpci(CURP, reset=True)
    assert server.last["headers"]["x-sandbox"] == "true"
    assert server.last["headers"]["x-reset"] == "true"
    apimarket.get_rpci(CURP)
    assert "x-reset" not in server.last["headers"]


def test_async_template_generation(server):
    apimarket.generate_from_template("9", [{"a": "b"}], wait=False)
    assert server.last["query"] == {"wait": "false"}
    assert server.last["headers"]["x-wait-for-completion"] == "false"


def test_consecutive_sync_calls(server):
    for _ in range(3):
        apimarket.get_balance()
    assert len(server.requests) == 3


def test_concurrent_async_calls_keep_their_arguments(server):
    connect(server, async_client=True)

    async def run():
        await asyncio.gather(apimarket.get_assigned_umf(NSS), apimarket.get_nss_data("92919084431"),
                             apimarket.check_sat_rfc(RFC))

    asyncio.run(run())
    received = sorted((r["path"], tuple(r["query"].values())) for r in server.requests)
    assert received == [
        ("/api/imss/grupo/obtener-datos-nss", ("92919084431",)),
        ("/api/imss/grupo/umf-asignada", (NSS,)),
        ("/api/sat/grupo/validar-rfc", (RFC,)),
    ]


# Las funciones @format_api comparten la configuración que inyecta kink.
POSTAL_CODES = [f"{number:05d}" for number in range(10000, 10040)]


def test_concurrent_async_format_api_calls_keep_their_arguments(server):
    connect(server, async_client=True)

    async def run():
        await asyncio.gather(*(apimarket.locate_umf_by_cp(cp) for cp in POSTAL_CODES),
                             apimarket.locate_nss_by_curp(CURP))

    asyncio.run(run())
    assert sorted(r["query"]["cp"] for r in server.requests if "cp" in r["query"]) == POSTAL_CODES
    assert [r["query"] for r in server.requests if r["path"].endswith("localizar-nss")] == [{"curp": CURP}]


def test_pending_format_api_call_is_not_modified_by_the_next_one(server):
    connect(server, async_client=True)
    first = apimarket.locate_umf_by_cp("11111")
    second = apimarket.locate_umf_by_cp("22222")

    async def run():
        await first
        await second

    asyncio.run(run())
    assert [r["query"] for r in server.requests] == [{"cp": "11111"}, {"cp": "22222"}]


def test_threaded_format_api_calls_keep_their_arguments(server):
    with ThreadPoolExecutor(8) as pool:
        list(pool.map(apimarket.locate_umf_by_cp, POSTAL_CODES * 3))
    assert sorted(r["query"]["cp"] for r in server.requests) == sorted(POSTAL_CODES * 3)


@pytest.mark.parametrize("argv", [
    ["-vc", CURP], ["-ro", CURP], ["-lu", "01000"], ["-pm"], ["-lc"],
    ["-c", CURP], ["-gt", "n", "e", "d", "permiso", "", ""],
])
def test_legacy_cli_shows_api_errors_without_traceback(server, capsys, argv):
    payload = {"success": False, "codigoValidacion": "ABC123", "message": "El token no es valido.", "status": 401}
    server.reply = (401, "application/json", json.dumps(payload).encode())
    with pytest.raises(SystemExit) as exit_:
        main(argv)
    assert exit_.value.code == 1
    assert len(server.requests) == 1
    captured = capsys.readouterr()
    assert "(status 401)" in captured.err
    assert "Traceback" not in captured.err
    if argv != ["-lc"]:  # IDSE Pro no comparte el formato de error de API Market
        assert "Error [API_KEY_UNAUTHORIZED]: El token no es valido. (status 401)" in captured.err
        assert '"codigoValidacion"' in captured.out and "ABC123" in captured.out


def test_legacy_cli_reports_connection_errors(server, capsys):
    di[ApiMarketClient].request_adapter.base_url = "http://127.0.0.1:1"
    with pytest.raises(SystemExit) as exit_:
        main(["-lu", "01000"])
    assert exit_.value.code == 1
    assert "Error [NETWORK_CONNECTION_ERROR]: No fue posible conectar" in capsys.readouterr().err

