import pytest
import apimarket
from kiota_abstractions.api_error import APIError

from cases import cases_for
from support import check_cli, check_request


class TestGeoRequests:
    @pytest.mark.parametrize(**cases_for("geo"))
    def test_function_sends_request(self, server, name, arguments, expected):
        check_request(server, name, arguments, expected)

    @pytest.mark.parametrize(**cases_for("geo"))
    def test_cli_sends_request(self, server, tmp_path, capsys, name, arguments, expected):
        check_cli(server, tmp_path, capsys, name, arguments, expected)


@pytest.mark.integracion
class TestGeoIntegration:
    """Consultas de solo lectura en modo sandbox contra la API real."""

    @pytest.mark.parametrize("call", [
        lambda: apimarket.search_postal_codes(postal_code="eq.10001", country_code="eq.US"),
    ])
    def test_reaches_api_without_validation_error(self, sdk_sandbox, call):
        try:
            assert call() is not None
        except APIError:
            pass  # Datos de prueba rechazados por la API: comportamiento esperado
