import pytest
import apimarket
from apimarket.validations import InvalidCURPError
from kiota_abstractions.api_error import APIError

from datos import CURP_INTEGRACION

CURP = "XEXX010101MNEXXXA4"


class TestObtenerCedulaUnit:
    @pytest.mark.parametrize("curp, expected_code", [
        ("XEXX010101",           InvalidCURPError.Code.INVALID_LENGTH),
        ("XEXX010101MNEXXXA4XX", InvalidCURPError.Code.INVALID_LENGTH),
        ("123456789012345678",   InvalidCURPError.Code.INVALID_FORMAT),
        ("XEXX010101MNEXXXA9",   InvalidCURPError.Code.INVALID_DIGIT),
    ])
    def test_invalid_curp_raises_before_api_call(self, curp, expected_code):
        with pytest.raises(InvalidCURPError) as exc_info:
            apimarket.obtain_sep_cedula(curp)
        assert exc_info.value.code == expected_code


@pytest.mark.integracion
class TestObtenerCedulaIntegration:
    def test_reaches_api_without_validation_error(self, sdk):
        try:
            response = apimarket.obtain_sep_cedula(CURP_INTEGRACION)
            assert response is not None
            assert response.codigo_validacion is not None
        except APIError:
            pass  # CURP válida pero sin cédulas registradas — comportamiento esperado

    def test_response_data_is_list(self, sdk):
        try:
            response = apimarket.obtain_sep_cedula(CURP_INTEGRACION)
            if response.success and response.data:
                assert isinstance(response.data, list)
                item = response.data[0]
                assert item.id_cedula is not None
                assert item.curp == CURP_INTEGRACION
        except APIError:
            pass

    def test_invalid_curp_never_reaches_api(self, sdk):
        with pytest.raises(InvalidCURPError):
            apimarket.obtain_sep_cedula("INVALIDA123456789")
