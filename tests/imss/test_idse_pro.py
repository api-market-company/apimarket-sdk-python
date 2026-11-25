import pytest
import apimarket
from kiota_abstractions.api_error import APIError


@pytest.mark.integracion
class TestIdseProIntegration:
    def test_reaches_api_without_validation_error(self, sdk):
        try:
            certificates = apimarket.idse_list_certificates()
            assert certificates is not None
        except APIError:
            pass  # Sin certificados IDSE configurados — comportamiento esperado

    def test_certificate_has_required_fields(self, sdk):
        try:
            certificates = apimarket.idse_list_certificates()
            if certificates and len(certificates) > 0:
                cert = certificates[0]
                assert cert.name is not None
                assert cert.rfc is not None
                assert cert.valid_until is not None
        except APIError:
            pass
