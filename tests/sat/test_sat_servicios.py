import pytest
import apimarket
from apimarket.validations import InvalidFileError, InvalidParameterError, InvalidRFCError
from kiota_abstractions.api_error import APIError

from cases import RFC, cases_for
from support import check_cli, check_request


class TestSatRequests:
    @pytest.mark.parametrize(**cases_for("sat"))
    def test_function_sends_request(self, server, name, arguments, expected):
        check_request(server, name, arguments, expected)

    @pytest.mark.parametrize(**cases_for("sat"))
    def test_cli_sends_request(self, server, tmp_path, capsys, name, arguments, expected):
        check_cli(server, tmp_path, capsys, name, arguments, expected)


class TestSatUnit:
    @pytest.mark.parametrize("call, error, code", [
        (lambda: apimarket.check_sat_rfc("MAL"),
         InvalidRFCError, InvalidRFCError.Code.INVALID_FORMAT),
        (lambda: apimarket.get_rfc_certificates("MAL"),
         InvalidRFCError, InvalidRFCError.Code.INVALID_FORMAT),
        (lambda: apimarket.get_fiscal_data_by_idcif("XAXX010101000", ""),
         InvalidParameterError, InvalidParameterError.Code.IDCIF_MISSING),
        (lambda: apimarket.validate_sat_receiver("XAXX010101000", "", "01000", "601"),
         InvalidParameterError, InvalidParameterError.Code.NOMBRE_MISSING),
        (lambda: apimarket.parse_csf(b""),
         InvalidFileError, InvalidFileError.Code.CSF_FILE_EMPTY),
        (lambda: apimarket.verify_sat_signature("MAL", "p", b"c", b"k"),
         InvalidRFCError, InvalidRFCError.Code.INVALID_FORMAT),
        (lambda: apimarket.read_sat_message(""),
         InvalidParameterError, InvalidParameterError.Code.UUID_MISSING),
        (lambda: apimarket.read_sat_message(".."),
         InvalidParameterError, InvalidParameterError.Code.UUID_PATH),
        (lambda: apimarket.download_sat_invoice("550e8400-e29b-41d4-a716-446655440000", ""),
         InvalidParameterError, InvalidParameterError.Code.BLOB_PATH_MISSING),
    ])
    def test_invalid_data_never_reaches_api(self, server, call, error, code):
        with pytest.raises(error) as exc_info:
            call()
        assert exc_info.value.code == code
        assert exc_info.value.message
        assert server.requests == []


@pytest.mark.integracion
class TestSatIntegration:
    """Consultas de solo lectura en modo sandbox contra la API real."""

    @pytest.mark.parametrize("call", [
        lambda: apimarket.check_sat_rfc(RFC),
        lambda: apimarket.get_rfc_certificates(RFC),
        lambda: apimarket.get_sat_tax_returns(2024),
    ])
    def test_reaches_api_without_validation_error(self, sdk_sandbox, call):
        try:
            assert call() is not None
        except APIError:
            pass  # Datos de prueba rechazados por la API: comportamiento esperado
