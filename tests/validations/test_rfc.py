import pytest
from apimarket.validations import validate_rfc, InvalidRFCError


class TestValidateRfc:
    @pytest.mark.parametrize("rfc", [
        "GOAJ900101AB1",
        "SAT990101NI5",
    ])
    def test_valid_rfc(self, rfc):
        assert validate_rfc(rfc) == rfc

    @pytest.mark.parametrize("rfc", [
        "GOA900101",
        "goaj900101ab1",
        "INVALIDO",
    ])
    def test_invalid_rfc_raises_invalid_format(self, rfc):
        with pytest.raises(InvalidRFCError) as exc_info:
            validate_rfc(rfc)
        assert exc_info.value.code == InvalidRFCError.Code.INVALID_FORMAT
        assert "RFC" in exc_info.value.message

    def test_error_string_format(self):
        with pytest.raises(InvalidRFCError) as exc_info:
            validate_rfc("INVALIDO")
        assert "INVALID_RFC_FORMAT" in str(exc_info.value)
