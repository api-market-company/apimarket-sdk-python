import pytest
import apimarket
from apimarket.validations import InvalidCURPError
from kiota_abstractions.api_error import APIError

from cases import cases_for
from support import check_cli, check_request

from datos import CURP_INTEGRACION


class TestRenapoRequests:
    @pytest.mark.parametrize(**cases_for("renapo"))
    def test_function_sends_request(self, server, name, arguments, expected):
        check_request(server, name, arguments, expected)

    @pytest.mark.parametrize(**cases_for("renapo"))
    def test_cli_sends_request(self, server, tmp_path, capsys, name, arguments, expected):
        check_cli(server, tmp_path, capsys, name, arguments, expected)


class TestRenapoUnit:
    @pytest.mark.parametrize("call, error, code", [
        (lambda: apimarket.get_birth_certificate("CORTA"),
         InvalidCURPError, InvalidCURPError.Code.INVALID_LENGTH),
    ])
    def test_invalid_data_never_reaches_api(self, server, call, error, code):
        with pytest.raises(error) as exc_info:
            call()
        assert exc_info.value.code == code
        assert exc_info.value.message
        assert server.requests == []


@pytest.mark.integracion
class TestRenapoIntegration:
    """Consultas de solo lectura en modo sandbox contra la API real."""

    @pytest.mark.parametrize("call", [
        lambda: apimarket.get_birth_certificate(CURP_INTEGRACION),
    ])
    def test_reaches_api_without_validation_error(self, sdk_sandbox, call):
        try:
            assert call() is not None
        except APIError:
            pass  # Datos de prueba rechazados por la API: comportamiento esperado
