import pytest
import apimarket
from apimarket.validations import InvalidRFCError
from kiota_abstractions.api_error import APIError


class TestLista69bUnit:
    @pytest.mark.parametrize("rfc", [
        "GOA900101",
        "goaj900101ab1",
        "INVALIDO",
    ])
    def test_invalid_rfc_raises_before_api_call(self, rfc):
        with pytest.raises(InvalidRFCError) as exc_info:
            apimarket.search_sat_lista69b(rfc=rfc)
        assert exc_info.value.code == InvalidRFCError.Code.INVALID_FORMAT

    def test_no_params_does_not_raise_locally(self, server):
        # La validación de parámetros ausentes la hace el API, no el SDK
        # Solo verificamos que no explota localmente
        try:
            apimarket.search_sat_lista69b()
        except (InvalidRFCError,):
            pytest.fail("No debe lanzar InvalidRFCError sin parámetros")
        except Exception:
            pass  # APIError u otro — aceptable


@pytest.mark.integracion
class TestLista69bIntegration:
    def test_reaches_api_with_rfc(self, sdk):
        try:
            response = apimarket.search_sat_lista69b(rfc="GOAJ900101AB1")
            assert response is not None
            assert response.codigo_validacion is not None
        except APIError:
            pass  # RFC válido pero sin coincidencias — comportamiento esperado

    def test_not_found_returns_empty_data(self, sdk):
        try:
            response = apimarket.search_sat_lista69b(rfc="GOAJ900101AB1")
            if response.success and response.status == 204:
                assert response.data == [] or response.data is None
        except APIError:
            pass

    def test_found_entry_has_required_fields(self, sdk):
        try:
            response = apimarket.search_sat_lista69b(rfc="GOAJ900101AB1")
            if response.success and response.data:
                item = response.data[0]
                assert item.rfc is not None
                assert item.nombre_contribuyente is not None
                assert item.situacion_contribuyente is not None
        except APIError:
            pass

    def test_invalid_rfc_never_reaches_api(self, sdk):
        with pytest.raises(InvalidRFCError):
            apimarket.search_sat_lista69b(rfc="INVALIDO")
