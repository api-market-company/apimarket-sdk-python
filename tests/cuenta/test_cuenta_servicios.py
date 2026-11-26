import pytest
import apimarket
from apimarket.validations import InvalidParameterError, InvalidRFCError
from kiota_abstractions.api_error import APIError

from cases import cases_for
from support import check_cli, check_request


class TestCuentaRequests:
    @pytest.mark.parametrize(**cases_for("cuenta"))
    def test_function_sends_request(self, server, name, arguments, expected):
        check_request(server, name, arguments, expected)

    @pytest.mark.parametrize(**cases_for("cuenta"))
    def test_cli_sends_request(self, server, tmp_path, capsys, name, arguments, expected):
        check_cli(server, tmp_path, capsys, name, arguments, expected)


class TestCuentaUnit:
    @pytest.mark.parametrize("call, error, code", [
        (lambda: apimarket.store_token("", permissions=["a"]),
         InvalidParameterError, InvalidParameterError.Code.NAME_MISSING),
        (lambda: apimarket.store_token("nombre"),
         InvalidParameterError, InvalidParameterError.Code.PERMISSIONS_MISSING),
        (lambda: apimarket.store_token("n", permissions=["a"], rfc="MAL"),
         InvalidRFCError, InvalidRFCError.Code.INVALID_FORMAT),
    ])
    def test_invalid_data_never_reaches_api(self, server, call, error, code):
        with pytest.raises(error) as exc_info:
            call()
        assert exc_info.value.code == code
        assert exc_info.value.message
        assert server.requests == []


@pytest.mark.integracion
class TestCuentaIntegration:
    """Consultas de solo lectura en modo sandbox contra la API real."""

    @pytest.mark.parametrize("call", [
        lambda: apimarket.get_balance(),
        lambda: apimarket.get_public_key(),
    ])
    def test_reaches_api_without_validation_error(self, sdk_sandbox, call):
        try:
            assert call() is not None
        except APIError:
            pass  # Datos de prueba rechazados por la API: comportamiento esperado
