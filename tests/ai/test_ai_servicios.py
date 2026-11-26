import pytest
import apimarket
from apimarket.validations import InvalidFileError, InvalidParameterError
from kiota_abstractions.api_error import APIError

from cases import cases_for
from support import check_cli, check_request


class TestAiRequests:
    @pytest.mark.parametrize(**cases_for("ai"))
    def test_function_sends_request(self, server, name, arguments, expected):
        check_request(server, name, arguments, expected)

    @pytest.mark.parametrize(**cases_for("ai"))
    def test_cli_sends_request(self, server, tmp_path, capsys, name, arguments, expected):
        check_cli(server, tmp_path, capsys, name, arguments, expected)


class TestAiUnit:
    @pytest.mark.parametrize("call, error, code", [
        (lambda: apimarket.ocr_id(b""),
         InvalidFileError, InvalidFileError.Code.ANVERSO_FILE_EMPTY),
        (lambda: apimarket.create_template(b""),
         InvalidFileError, InvalidFileError.Code.TEMPLATE_FILE_EMPTY),
        (lambda: apimarket.generate_from_template("9", []),
         InvalidParameterError, InvalidParameterError.Code.INPUTS_MISSING),
        (lambda: apimarket.smart_processing_estimate(""),
         InvalidParameterError, InvalidParameterError.Code.DATASET_MISSING),
        (lambda: apimarket.smart_processing_delete("."),
         InvalidParameterError, InvalidParameterError.Code.RESOURCE_PATH),
        (lambda: apimarket.get_dataset_rows(""),
         InvalidParameterError, InvalidParameterError.Code.RESOURCE_MISSING),
    ])
    def test_invalid_data_never_reaches_api(self, server, call, error, code):
        with pytest.raises(error) as exc_info:
            call()
        assert exc_info.value.code == code
        assert exc_info.value.message
        assert server.requests == []


@pytest.mark.integracion
class TestAiIntegration:
    """Consultas de solo lectura en modo sandbox contra la API real."""

    @pytest.mark.parametrize("call", [
        lambda: apimarket.list_datasets(),
        lambda: apimarket.smart_processing_status(),
    ])
    def test_reaches_api_without_validation_error(self, sdk_sandbox, call):
        try:
            assert call() is not None
        except APIError:
            pass  # Datos de prueba rechazados por la API: comportamiento esperado
