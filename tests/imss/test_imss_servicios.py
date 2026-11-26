import pytest
import apimarket
from apimarket.validations import InvalidCURPError, InvalidNSSError, InvalidParameterError
from kiota_abstractions.api_error import APIError

from cases import NSS, cases_for
from support import check_cli, check_request

from datos import CURP_INTEGRACION


class TestImssRequests:
    @pytest.mark.parametrize(**cases_for("imss"))
    def test_function_sends_request(self, server, name, arguments, expected):
        check_request(server, name, arguments, expected)

    @pytest.mark.parametrize(**cases_for("imss"))
    def test_cli_sends_request(self, server, tmp_path, capsys, name, arguments, expected):
        check_cli(server, tmp_path, capsys, name, arguments, expected)


class TestImssUnit:
    @pytest.mark.parametrize("call, error, code", [
        (lambda: apimarket.get_imss_pension("123"),
         InvalidNSSError, InvalidNSSError.Code.INVALID_LENGTH),
        (lambda: apimarket.get_assigned_umf("123"),
         InvalidNSSError, InvalidNSSError.Code.INVALID_LENGTH),
        (lambda: apimarket.get_nss_data("123"),
         InvalidNSSError, InvalidNSSError.Code.INVALID_LENGTH),
        (lambda: apimarket.get_rpci("CORTA"),
         InvalidCURPError, InvalidCURPError.Code.INVALID_LENGTH),
        (lambda: apimarket.get_labor_history_lite("CORTA", "a@example.com"),
         InvalidCURPError, InvalidCURPError.Code.INVALID_LENGTH),
        (lambda: apimarket.get_labor_history_lite("XEXX010101MNEXXXA4", ""),
         InvalidParameterError, InvalidParameterError.Code.EMAIL_MISSING),
        (lambda: apimarket.get_employment_trajectory(""),
         InvalidParameterError, InvalidParameterError.Code.IDENTIFICADOR_MISSING),
        (lambda: apimarket.idse_capture_movements([], "https://example.com"),
         InvalidParameterError, InvalidParameterError.Code.MOVIMIENTOS_MISSING),
        (lambda: apimarket.idse_get_movements_status(1, "https://example.com", {}, "abc"),
         InvalidParameterError, InvalidParameterError.Code.CREDENTIALS_MISSING),
        (lambda: apimarket.idse_get_employer_registrations(""),
         InvalidParameterError, InvalidParameterError.Code.WEBHOOK_MISSING),
    ])
    def test_invalid_data_never_reaches_api(self, server, call, error, code):
        with pytest.raises(error) as exc_info:
            call()
        assert exc_info.value.code == code
        assert exc_info.value.message
        assert server.requests == []


@pytest.mark.integracion
class TestImssIntegration:
    """Consultas de solo lectura en modo sandbox contra la API real."""

    @pytest.mark.parametrize("call", [
        lambda: apimarket.get_imss_pension(NSS),
        lambda: apimarket.get_assigned_umf(NSS),
        lambda: apimarket.get_nss_data(NSS),
        lambda: apimarket.get_rpci(CURP_INTEGRACION),
    ])
    def test_reaches_api_without_validation_error(self, sdk_sandbox, call):
        try:
            assert call() is not None
        except APIError:
            pass  # Datos de prueba rechazados por la API: comportamiento esperado
