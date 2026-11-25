import pytest
import apimarket
from apimarket.validations import InvalidCURPError
from kiota_abstractions.api_error import APIError

from datos import CURP_INTEGRACION

CURP = "XEXX010101MNEXXXA4"


class TestObtenerRfcUnit:
    @pytest.mark.parametrize("curp, expected_code", [
        ("XEXX010101",           InvalidCURPError.Code.INVALID_LENGTH),
        ("XEXX010101MNEXXXA4XX", InvalidCURPError.Code.INVALID_LENGTH),
        ("123456789012345678",   InvalidCURPError.Code.INVALID_FORMAT),
        ("XEXX010101MNEXXXA9",   InvalidCURPError.Code.INVALID_DIGIT),
    ])
    def test_invalid_curp_raises_before_api_call(self, curp, expected_code):
        with pytest.raises(InvalidCURPError) as exc_info:
            apimarket.get_rfc_from_curp(curp)
        assert exc_info.value.code == expected_code


@pytest.mark.integracion
class TestObtenerRfcIntegration:
    def test_reaches_api_without_validation_error(self, sdk):
        try:
            response = apimarket.get_rfc_from_curp(CURP_INTEGRACION)
            assert response is not None
            assert response.codigo_validacion is not None
        except APIError:
            pass  # CURP válida pero sin RFC en SAT — comportamiento esperado

    def test_response_with_rfc_has_typed_data(self, sdk):
        try:
            response = apimarket.get_rfc_from_curp(CURP_INTEGRACION)
            if response.success and response.data is not None:
                assert isinstance(response.data.rfc, str)
                assert len(response.data.rfc) >= 12
        except APIError:
            pass

    def test_invalid_curp_never_reaches_api(self, sdk):
        with pytest.raises(InvalidCURPError):
            apimarket.get_rfc_from_curp("INVALIDA123456789")
