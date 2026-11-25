import pytest
from apimarket.validations import validate_curp, InvalidCURPError


class TestValidateCurp:
    @pytest.mark.parametrize("curp", [
        "XEXX010101MNEXXXA4",
    ])
    def test_valid_curp(self, curp):
        assert validate_curp(curp) == curp

    @pytest.mark.skip(reason="Pending: need a real CURP whose check digit is 0")
    def test_curp_with_zero_check_digit_is_valid(self):
        # Covers the digit==10 branch in calculate_curp_verification_digit
        curp = "REEMPLAZAR_CON_CURP_REAL"
        assert validate_curp(curp) == curp

    @pytest.mark.parametrize("curp, expected_code, message_fragment", [
        ("XEXX010101",           InvalidCURPError.Code.INVALID_LENGTH, "18 caracteres"),
        ("XEXX010101MNEXXXA4XX", InvalidCURPError.Code.INVALID_LENGTH, "18 caracteres"),
        ("123456789012345678",   InvalidCURPError.Code.INVALID_FORMAT, "formato"),
        ("XEXX010101MNEXXXA9",   InvalidCURPError.Code.INVALID_DIGIT,  "Dígito verificador"),
    ])
    def test_invalid_curp(self, curp, expected_code, message_fragment):
        with pytest.raises(InvalidCURPError) as exc_info:
            validate_curp(curp)
        assert exc_info.value.code == expected_code
        assert message_fragment in exc_info.value.message

    def test_error_string_format(self):
        with pytest.raises(InvalidCURPError) as exc_info:
            validate_curp("XEXX010101")
        assert "INVALID_CURP_LENGTH" in str(exc_info.value)
