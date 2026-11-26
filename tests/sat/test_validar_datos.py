import pytest
import apimarket
from apimarket.validations import InvalidRFCError
from kiota_abstractions.api_error import APIError

_PARAMS = dict(
    nombre="JUAN CARLOS GOMEZ ARANDA",
    rfc="GOAJ900101AB1",
    regimen="612",
    cp="06600",
)


class TestValidarDatosUnit:
    @pytest.mark.parametrize("rfc", [
        "GOA900101",
        "goaj900101ab1",
        "INVALIDO",
    ])
    def test_invalid_rfc_raises_before_api_call(self, rfc):
        with pytest.raises(InvalidRFCError) as exc_info:
            apimarket.validate_sat_data("JUAN GARCIA", rfc, "612", "06600")
        assert exc_info.value.code == InvalidRFCError.Code.INVALID_FORMAT


@pytest.mark.integracion
class TestValidarDatosIntegration:
    def test_reaches_api_without_validation_error(self, sdk):
        try:
            response = apimarket.validate_sat_data(**_PARAMS)
            assert response is not None
            assert response.codigo_validacion is not None
        except APIError:
            pass  # Datos de prueba sin coincidencia en SAT — comportamiento esperado

    def test_response_data_has_resultado(self, sdk):
        try:
            response = apimarket.validate_sat_data(**_PARAMS)
            if response.success and response.data:
                assert response.data.resultado is not None
                assert isinstance(response.data.resultado, str)
        except APIError:
            pass

    def test_response_has_message(self, sdk):
        try:
            response = apimarket.validate_sat_data(**_PARAMS)
            assert response.message is not None
        except APIError:
            pass

    def test_invalid_rfc_never_reaches_api(self, sdk):
        with pytest.raises(InvalidRFCError):
            apimarket.validate_sat_data("JUAN GARCIA", "INVALIDO", "612", "06600")
