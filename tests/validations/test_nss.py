import pytest
from apimarket.validations import validate_nss, InvalidNSSError


class TestValidateNss:
    def test_valid_nss(self):
        nss = "12345678952"
        assert validate_nss(nss) == nss

    @pytest.mark.parametrize("nss, expected_code, message_fragment", [
        ("1234567",      InvalidNSSError.Code.INVALID_LENGTH, "11 dígitos"),
        ("1234567890A",  InvalidNSSError.Code.INVALID_FORMAT, "dígitos"),
        ("12345678900",  InvalidNSSError.Code.INVALID_DIGIT,  "Dígito verificador"),
    ])
    def test_invalid_nss(self, nss, expected_code, message_fragment):
        with pytest.raises(InvalidNSSError) as exc_info:
            validate_nss(nss)
        assert exc_info.value.code == expected_code
        assert message_fragment in exc_info.value.message

    def test_short_nss_message_includes_received_count(self):
        with pytest.raises(InvalidNSSError) as exc_info:
            validate_nss("1234567")
        assert "7" in exc_info.value.message

    def test_error_string_format(self):
        with pytest.raises(InvalidNSSError) as exc_info:
            validate_nss("1234567")
        assert "INVALID_NSS_LENGTH" in str(exc_info.value)
