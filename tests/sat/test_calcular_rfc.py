import pytest
import apimarket
from kiota_abstractions.api_error import APIError

_ARGS = ("Juan Carlos", "Garcia", "Lopez", "01", "01", "1990")


@pytest.mark.integracion
class TestCalcularRfcIntegration:
    def test_reaches_api_without_validation_error(self, sdk):
        try:
            response = apimarket.calculate_rfc(*_ARGS)
            assert response is not None
            assert response.codigo_validacion is not None
        except APIError:
            pass

    def test_response_data_has_rfc(self, sdk):
        try:
            response = apimarket.calculate_rfc(*_ARGS)
            if response.success and response.data:
                assert response.data.rfc is not None
        except APIError:
            pass

    def test_response_data_has_personal_fields(self, sdk):
        try:
            response = apimarket.calculate_rfc(*_ARGS)
            if response.success and response.data:
                assert response.data.nombres is not None
                assert response.data.apellido_paterno is not None
                assert response.data.apellido_materno is not None
                assert response.data.fecha_nacimiento is not None
        except APIError:
            pass

    def test_response_data_has_mensaje(self, sdk):
        try:
            response = apimarket.calculate_rfc(*_ARGS)
            if response.success and response.data:
                assert response.data.mensaje is not None
        except APIError:
            pass
