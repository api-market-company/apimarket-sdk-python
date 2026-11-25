"""El catálogo de códigos está completo y documentado."""
import enum
import pathlib
import re

import httpx
import pytest

import apimarket
from apimarket import errors, validations
from apimarket.cli import main
from apimarket.errors import CATALOG, ErrorCode, api_error_code
from apimarket.validations import ConfigurationError, InvalidFileError, InvalidParameterError, ValidationError

import fuzz
from cases import CURP


def all_codes():
    codes = set(ErrorCode)
    for name in dir(validations):
        value = getattr(validations, name)
        if isinstance(value, type) and issubclass(value, ValidationError):
            inner = getattr(value, "Code", None)
            if isinstance(inner, type) and issubclass(inner, enum.Enum):
                codes |= set(inner)
    return codes


def test_catalog_lists_every_code_once():
    listed = [code for _, _, codes in CATALOG for code, _ in codes]
    assert set(listed) == all_codes()
    values = [code.value for code in listed]
    assert len(values) == len(set(values))


def test_field_table_matches_the_validators():
    found, unexpected = fuzz.run()
    assert unexpected == []  # ningún dato inválido produce un error sin código
    produced = {code for code in found if isinstance(code, (InvalidParameterError.Code, InvalidFileError.Code))}
    # La plantilla de 500 MB se comprueba en test_error_codes.py.
    declared = {*InvalidParameterError.Code, *InvalidFileError.Code} - {InvalidFileError.Code.TEMPLATE_FILE_SIZE}
    assert produced == declared


@pytest.mark.parametrize("pattern, codes", [
    (r"INVALID_[A-Z0-9_]+_(LENGTH|FORMAT|DIGIT|MISSING|TYPE|RANGE|OPTION|COMBINATION|PATH|NOT_FOUND|UNREADABLE|EMPTY"
     r"|SIZE|CONTENT)", lambda: all_codes() - set(ErrorCode) - set(ConfigurationError.Code)),
    (r"(API|NETWORK|CLI)_[A-Z]+(_[A-Z]+)+", lambda: set(ErrorCode)),
    (r"CONFIG_[A-Z_]+_MISSING", lambda: set(ConfigurationError.Code)),
])
def test_codes_follow_the_naming_format(pattern, codes):
    assert [code.value for code in codes() if not re.fullmatch(pattern, code.value)] == []


def test_documentation_lists_every_code():
    document = pathlib.Path(__file__).parents[2].joinpath("docs/error_catalog.rst").read_text(encoding="utf-8")
    assert [code.value for code in all_codes() if f"``{code.value}``" not in document] == []


@pytest.mark.parametrize("status, code", [
    (400, ErrorCode.API_REQUEST_INVALID), (401, ErrorCode.API_KEY_UNAUTHORIZED), (402, ErrorCode.API_PAYMENT_REQUIRED),
    (403, ErrorCode.API_PERMISSION_FORBIDDEN), (404, ErrorCode.API_RESOURCE_NOT_FOUND), (409, ErrorCode.API_REQUEST_FAILED),
    (422, ErrorCode.API_REQUEST_UNPROCESSABLE), (429, ErrorCode.API_REQUEST_LIMIT_EXCEEDED), (500, ErrorCode.API_SERVER_ERROR),
    (503, ErrorCode.API_SERVICE_UNAVAILABLE),
])
def test_status_codes(status, code):
    assert api_error_code(status) is code


@pytest.mark.parametrize("call", [
    lambda: apimarket.locate_umf_by_cp("06600"), lambda: apimarket.get_assigned_umf("12345678903"),
])
@pytest.mark.parametrize("status, code", [(401, ErrorCode.API_KEY_UNAUTHORIZED), (403, ErrorCode.API_PERMISSION_FORBIDDEN)])
def test_old_and_new_api_errors_carry_a_code(server, call, status, code):
    server.reply = (status, "application/json", b'{"status":%d,"success":false,"message":"m"}' % status)
    with pytest.raises(errors.APIError) as exc_info:
        call()
    assert exc_info.value.code is code


@pytest.mark.parametrize("call", [
    lambda: apimarket.locate_umf_by_cp("06600"), lambda: apimarket.get_assigned_umf("12345678903"),
])
def test_connection_errors_carry_a_code(server, call):
    from kink import di
    from apimarket.api_market_client import ApiMarketClient
    di[ApiMarketClient].request_adapter.base_url = "http://127.0.0.1:1"
    with pytest.raises(httpx.HTTPError) as exc_info:
        call()
    assert exc_info.value.code is ErrorCode.NETWORK_CONNECTION_ERROR


def test_provider_failure_inside_http_200(server, capsys):
    server.reply = (200, "application/json", b'{"status":503,"success":true,"message":"El SAT no responde."}')
    with pytest.raises(apimarket.ApiMarketError) as exc_info:
        apimarket.get_sat_information()
    assert exc_info.value.code is ErrorCode.API_SERVICE_UNAVAILABLE
    with pytest.raises(SystemExit):
        main(["-lu", "06600"])
    assert "Error [API_SERVICE_UNAVAILABLE]: El SAT no responde." in capsys.readouterr().err


def test_unreadable_response(server):
    server.reply = (200, "application/json", b"{roto")
    with pytest.raises(apimarket.ApiMarketError) as exc_info:
        apimarket.get_balance()
    assert exc_info.value.code is ErrorCode.API_RESPONSE_INVALID


@pytest.mark.parametrize("call", [
    lambda: apimarket.fetch_curp_details(CURP), lambda: apimarket.get_balance(),
])
def test_missing_api_key(server, call):
    from kink import di
    di["API_MARKET_API_KEY"] = ""
    with pytest.raises(ConfigurationError) as exc_info:
        call()
    assert exc_info.value.code is ConfigurationError.Code.API_KEY_MISSING
    assert server.requests == []


@pytest.mark.parametrize("argv, code, exit_code", [
    (["-vc", "MALA"], "INVALID_CURP_LENGTH", 1),
    (["-lu", "1"], "INVALID_CP_LENGTH", 1),
    (["sat", "leer-csf", "--csf", "/no/existe"], "INVALID_CSF_FILE_NOT_FOUND", 1),
    (["sat", "declaraciones", "--year", "abc"], "CLI_ARGUMENTS_INVALID", 2),
    (["sat", "declaraciones"], "CLI_ARGUMENTS_INVALID", 2),
    (["--no-existe"], "CLI_ARGUMENTS_INVALID", 2),
    (["-vi", "1"], "CLI_ARGUMENTS_INVALID", 2),
])
def test_cli_always_prints_the_code(server, capsys, argv, code, exit_code):
    with pytest.raises(SystemExit) as exit_:
        main(argv)
    assert exit_.value.code == exit_code
    assert f"Error [{code}]:" in capsys.readouterr().err
    assert server.requests == []


def test_cli_prints_the_catalog(capsys):
    main(["errores"])
    output = capsys.readouterr().out
    assert all(code.value in output for code in all_codes())
