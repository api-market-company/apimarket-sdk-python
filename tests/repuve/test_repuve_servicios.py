import pytest
import apimarket
from apimarket.validations import InvalidParameterError
from kiota_abstractions.api_error import APIError

from cases import cases_for
from support import check_cli, check_request


class TestRepuveRequests:
    @pytest.mark.parametrize(**cases_for("repuve"))
    def test_function_sends_request(self, server, name, arguments, expected):
        check_request(server, name, arguments, expected)

    @pytest.mark.parametrize(**cases_for("repuve"))
    def test_cli_sends_request(self, server, tmp_path, capsys, name, arguments, expected):
        check_cli(server, tmp_path, capsys, name, arguments, expected)


class TestRepuveUnit:
    @pytest.mark.parametrize("call, error, code", [
        (lambda: apimarket.get_vehicle_owner(),
         InvalidParameterError, InvalidParameterError.Code.NUMERO_SERIE_PLACAS_MISSING),
        (lambda: apimarket.get_vehicle_data(),
         InvalidParameterError, InvalidParameterError.Code.NUMERO_SERIE_PLACAS_MISSING),
        (lambda: apimarket.check_vehicle_theft(),
         InvalidParameterError, InvalidParameterError.Code.NUMERO_SERIE_PLACAS_MISSING),
    ])
    def test_invalid_data_never_reaches_api(self, server, call, error, code):
        with pytest.raises(error) as exc_info:
            call()
        assert exc_info.value.code == code
        assert exc_info.value.message
        assert server.requests == []


@pytest.mark.integracion
class TestRepuveIntegration:
    """Consultas de solo lectura en modo sandbox contra la API real."""

    @pytest.mark.parametrize("call", [
        lambda: apimarket.get_vehicle_owner(placas="ABC1234"),
        lambda: apimarket.get_vehicle_data(placas="ABC1234"),
        lambda: apimarket.check_vehicle_theft(placas="ABC1234"),
    ])
    def test_reaches_api_without_validation_error(self, sdk_sandbox, call):
        try:
            assert call() is not None
        except APIError:
            pass  # Datos de prueba rechazados por la API: comportamiento esperado
