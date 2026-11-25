import pytest
import apimarket
from apimarket.validations import InvalidCURPError, InvalidNSSError
from kiota_abstractions.api_error import APIError

from datos import CURP_INTEGRACION

CURP_VALIDA = "XEXX010101MNEXXXA4"
NSS_VALIDO = "12345678952"


class TestImssUnit:
    @pytest.mark.parametrize("curp, expected_code", [
        ("CORTA",                InvalidCURPError.Code.INVALID_LENGTH),
        ("123456789012345678",   InvalidCURPError.Code.INVALID_FORMAT),
        ("XEXX010101MNEXXXA9",   InvalidCURPError.Code.INVALID_DIGIT),
    ])
    def test_locate_nss_invalid_curp_raises(self, curp, expected_code):
        with pytest.raises(InvalidCURPError) as exc_info:
            apimarket.locate_nss_by_curp(curp)
        assert exc_info.value.code == expected_code

    @pytest.mark.parametrize("nss, expected_code", [
        ("1234567",      InvalidNSSError.Code.INVALID_LENGTH),
        ("1234567890A",  InvalidNSSError.Code.INVALID_FORMAT),
        ("12345678900",  InvalidNSSError.Code.INVALID_DIGIT),
    ])
    def test_check_nss_validity_invalid_nss_raises(self, nss, expected_code):
        with pytest.raises(InvalidNSSError) as exc_info:
            apimarket.check_nss_validity(nss, CURP_VALIDA)
        assert exc_info.value.code == expected_code

    @pytest.mark.parametrize("curp, expected_code", [
        ("CORTA",                InvalidCURPError.Code.INVALID_LENGTH),
        ("XEXX010101MNEXXXA9",   InvalidCURPError.Code.INVALID_DIGIT),
    ])
    def test_get_clinic_by_curp_invalid_curp_raises(self, curp, expected_code):
        with pytest.raises(InvalidCURPError) as exc_info:
            apimarket.get_clinic_by_curp(curp)
        assert exc_info.value.code == expected_code


@pytest.mark.skip(reason="Endpoint deprecated — estado desconocido, puede no estar disponible")
@pytest.mark.integracion
class TestLocateUmfIntegration:
    def test_valid_cp_returns_response(self, sdk):
        response = apimarket.locate_umf_by_cp("06600")
        assert response is not None
        assert response.success is True
        assert response.codigo_validacion is not None

    def test_response_has_status(self, sdk):
        response = apimarket.locate_umf_by_cp("06600")
        assert response.status is not None


@pytest.mark.integracion
class TestLocateNssByCurpIntegration:
    def test_reaches_api_without_validation_error(self, sdk):
        # La CURP puede no tener NSS en IMSS — se acepta respuesta o error de API
        try:
            response = apimarket.locate_nss_by_curp(CURP_INTEGRACION)
            assert response is not None
            assert response.codigo_validacion is not None
        except APIError:
            pass  # CURP válida pero sin registro IMSS — comportamiento esperado

    def test_invalid_curp_never_reaches_api(self, sdk):
        with pytest.raises(InvalidCURPError):
            apimarket.locate_nss_by_curp("INVALIDA123456789")


@pytest.mark.integracion
class TestGetClinicByCurpIntegration:
    def test_reaches_api_without_validation_error(self, sdk):
        try:
            response = apimarket.get_clinic_by_curp(CURP_INTEGRACION)
            assert response is not None
            assert response.codigo_validacion is not None
        except APIError:
            pass  # CURP válida pero sin registro IMSS — comportamiento esperado

    def test_invalid_curp_never_reaches_api(self, sdk):
        with pytest.raises(InvalidCURPError):
            apimarket.get_clinic_by_curp("INVALIDA123456789")
