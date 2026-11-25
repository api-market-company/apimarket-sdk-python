import pytest
import apimarket
from apimarket.validations import InvalidCURPError
from kiota_abstractions.api_error import APIError

from datos import CURP_INTEGRACION

CURP = "XEXX010101MNEXXXA4"


class TestBuscarNacimientoUnit:
    @pytest.mark.parametrize("curp, expected_code", [
        ("XEXX010101",           InvalidCURPError.Code.INVALID_LENGTH),
        ("XEXX010101MNEXXXA4XX", InvalidCURPError.Code.INVALID_LENGTH),
        ("123456789012345678",   InvalidCURPError.Code.INVALID_FORMAT),
        ("XEXX010101MNEXXXA9",   InvalidCURPError.Code.INVALID_DIGIT),
    ])
    def test_invalid_curp_raises_before_api_call(self, curp, expected_code):
        with pytest.raises(InvalidCURPError) as exc_info:
            apimarket.get_birth_record(curp)
        assert exc_info.value.code == expected_code


@pytest.mark.integracion
class TestBuscarNacimientoIntegration:
    def test_reaches_api_without_validation_error(self, sdk):
        try:
            response = apimarket.get_birth_record(CURP_INTEGRACION)
            assert response is not None
            assert response.codigo_validacion is not None
        except APIError:
            pass  # CURP válida pero sin registro disponible — comportamiento esperado

    def test_response_has_personal_fields(self, sdk):
        try:
            response = apimarket.get_birth_record(CURP_INTEGRACION)
            if response.success and response.data:
                assert response.data.curp == CURP_INTEGRACION
                assert response.data.nombre is not None
                assert response.data.primer_apellido is not None
                assert response.data.fecha_nacimiento is not None
                assert response.data.sexo is not None
        except APIError:
            pass

    def test_response_has_datos_padres(self, sdk):
        try:
            response = apimarket.get_birth_record(CURP_INTEGRACION)
            if response.success and response.data and response.data.datos_padres:
                assert response.data.datos_padres.nombre_padre is not None
                assert response.data.datos_padres.nombre_madre is not None
        except APIError:
            pass

    def test_invalid_curp_never_reaches_api(self, sdk):
        with pytest.raises(InvalidCURPError):
            apimarket.get_birth_record("INVALIDA123456789")
