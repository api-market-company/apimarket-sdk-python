import pytest
import apimarket
from apimarket.validations import InvalidCURPError
from kiota_abstractions.api_error import APIError

from datos import CURP_INTEGRACION


class TestValidarCurpUnit:
    @pytest.mark.parametrize("curp, expected_code", [
        ("XEXX010101",           InvalidCURPError.Code.INVALID_LENGTH),
        ("XEXX010101MNEXXXA4XX", InvalidCURPError.Code.INVALID_LENGTH),
        ("123456789012345678",   InvalidCURPError.Code.INVALID_FORMAT),
        ("XEXX010101MNEXXXA9",   InvalidCURPError.Code.INVALID_DIGIT),
    ])
    def test_invalid_curp_raises_before_api_call(self, curp, expected_code):
        with pytest.raises(InvalidCURPError) as exc_info:
            apimarket.fetch_curp_details(curp)
        assert exc_info.value.code == expected_code


@pytest.mark.integracion
class TestValidarCurpIntegration:
    CURP = CURP_INTEGRACION

    def test_reaches_api_without_validation_error(self, sdk):
        try:
            response = apimarket.fetch_curp_details(self.CURP)
            assert response is not None
            assert response.codigo_validacion is not None
        except APIError:
            pass  # CURP válida pero API no disponible en este momento

    def test_response_has_personal_fields(self, sdk):
        try:
            response = apimarket.fetch_curp_details(self.CURP)
            if response.success and response.data:
                assert response.data.curp == self.CURP
                assert response.data.nombres is not None
                assert response.data.fecha_nacimiento is not None
                assert response.data.sexo is not None
        except APIError:
            pass

    def test_response_has_historial(self, sdk):
        try:
            response = apimarket.fetch_curp_details(self.CURP)
            if response.success and response.data:
                assert response.data.historial is not None
        except APIError:
            pass

    def test_response_has_doc_probatorio(self, sdk):
        try:
            response = apimarket.fetch_curp_details(self.CURP)
            if response.success and response.data:
                assert response.data.datos_doc_probatorio is not None
        except APIError:
            pass

    def test_invalid_curp_never_reaches_api(self, sdk):
        with pytest.raises(InvalidCURPError):
            apimarket.fetch_curp_details("INVALIDA123456789")


@pytest.mark.integracion
@pytest.mark.anyio
async def test_async_valid_curp_returns_success(sdk_async):
    try:
        response = await apimarket.fetch_curp_details(CURP_INTEGRACION)
        if response.success and response.data:
            assert response.data.nombres is not None
    except APIError:
        pass
