import pytest
import apimarket
from apimarket.validations import InvalidCreditError, InvalidNSSError, InvalidParameterError
from kiota_abstractions.api_error import APIError

from cases import cases_for
from support import check_cli, check_request


class TestInfonavitRequests:
    @pytest.mark.parametrize(**cases_for("infonavit"))
    def test_function_sends_request(self, server, name, arguments, expected):
        check_request(server, name, arguments, expected)

    @pytest.mark.parametrize(**cases_for("infonavit"))
    def test_cli_sends_request(self, server, tmp_path, capsys, name, arguments, expected):
        check_cli(server, tmp_path, capsys, name, arguments, expected)


class TestInfonavitUnit:
    @pytest.mark.parametrize("call, error, code", [
        (lambda: apimarket.get_infonavit_contact_data("123"),
         InvalidNSSError, InvalidNSSError.Code.INVALID_LENGTH),
        (lambda: apimarket.get_infonavit_technical_sheet(""),
         InvalidParameterError, InvalidParameterError.Code.IDENTIFICADOR_MISSING),
        (lambda: apimarket.get_infonavit_borrower_data(""),
         InvalidParameterError, InvalidParameterError.Code.IDENTIFICADOR_MISSING),
        (lambda: apimarket.get_infonavit_credit_history(""),
         InvalidParameterError, InvalidParameterError.Code.NUM_CREDITO_MISSING),
        (lambda: apimarket.get_infonavit_interest_report(""),
         InvalidParameterError, InvalidParameterError.Code.NUM_CREDITO_MISSING),
        (lambda: apimarket.get_infonavit_credit_history("123"),
         InvalidCreditError, InvalidCreditError.Code.INVALID_FORMAT),
        (lambda: apimarket.get_infonavit_financial_data("12345678901"),
         InvalidCreditError, InvalidCreditError.Code.INVALID_FORMAT),
        (lambda: apimarket.get_infonavit_collection_data("123456789A"),
         InvalidCreditError, InvalidCreditError.Code.INVALID_FORMAT),
        (lambda: apimarket.get_infonavit_credit_history_report("123"),
         InvalidCreditError, InvalidCreditError.Code.INVALID_FORMAT),
        (lambda: apimarket.get_infonavit_account_statement("1234 56789"),
         InvalidCreditError, InvalidCreditError.Code.INVALID_FORMAT),
        (lambda: apimarket.get_infonavit_interest_report("123"),
         InvalidCreditError, InvalidCreditError.Code.INVALID_FORMAT),
    ])
    def test_invalid_data_never_reaches_api(self, server, call, error, code):
        with pytest.raises(error) as exc_info:
            call()
        assert exc_info.value.code == code
        assert exc_info.value.message
        assert server.requests == []


@pytest.mark.integracion
class TestInfonavitIntegration:
    """Consultas de solo lectura en modo sandbox contra la API real."""

    @pytest.mark.parametrize("call", [
        lambda: apimarket.get_infonavit_credit_history("1234567890"),
    ])
    def test_reaches_api_without_validation_error(self, sdk_sandbox, call):
        try:
            assert call() is not None
        except APIError:
            pass  # Datos de prueba rechazados por la API: comportamiento esperado
