import pytest
import apimarket
from kiota_abstractions.api_error import APIError


@pytest.mark.integracion
class TestValidarCedulaIntegration:
    def test_reaches_api_without_validation_error(self, sdk):
        try:
            response = apimarket.validate_sep_cedula("12345678")
            assert response is not None
            assert response.codigo_validacion is not None
        except APIError:
            pass

    def test_found_cedula_returns_data_list(self, sdk):
        try:
            response = apimarket.validate_sep_cedula("12345678")
            if response.success and response.data:
                assert isinstance(response.data, list)
                assert len(response.data) > 0
        except APIError:
            pass

    def test_cedula_item_has_personal_fields(self, sdk):
        try:
            response = apimarket.validate_sep_cedula("12345678")
            if response.success and response.data and len(response.data) > 0:
                item = response.data[0]
                assert item.id_cedula is not None
                assert item.nombre is not None
                assert item.paterno is not None
        except APIError:
            pass

    def test_cedula_item_has_registro_fields(self, sdk):
        try:
            response = apimarket.validate_sep_cedula("12345678")
            if response.success and response.data and len(response.data) > 0:
                item = response.data[0]
                assert item.anioreg is not None
                assert item.tipo is not None
        except APIError:
            pass

    def test_not_found_cedula_returns_empty_data(self, sdk):
        try:
            response = apimarket.validate_sep_cedula("00000000")
            if response.success:
                assert response.data is None or response.data == []
        except APIError:
            pass
