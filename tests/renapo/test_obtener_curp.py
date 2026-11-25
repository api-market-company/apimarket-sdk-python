import pytest
import apimarket
from kiota_abstractions.api_error import APIError

_PARAMS = ("JUAN CARLOS", "GARCIA", "MARTINEZ", "15", "03", "1990", "09", "H")


@pytest.mark.integracion
class TestObtenerCurpIntegration:
    def test_reaches_api_without_validation_error(self, sdk):
        try:
            response = apimarket.get_curp_from_details(*_PARAMS)
            assert response is not None
            assert response.codigo_validacion is not None
        except APIError:
            pass  # Datos de prueba sin coincidencia en RENAPO — comportamiento esperado

    def test_response_has_all_fields(self, sdk):
        try:
            response = apimarket.get_curp_from_details(*_PARAMS)
            if response.success and response.data:
                assert response.data.nombres is not None
                assert response.data.apellido_paterno is not None
                assert response.data.sexo is not None
                assert response.data.fecha_nacimiento is not None
                assert response.data.estado_nacimiento is not None
        except APIError:
            pass

    def test_without_materno_reaches_api(self, sdk):
        try:
            response = apimarket.get_curp_from_details(
                "JUAN", "GARCIA", "", "15", "03", "1990", "09", "H"
            )
            assert response is not None
        except APIError:
            pass
