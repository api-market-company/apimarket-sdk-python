import pytest
from apimarket.validations import validate_birth_date, InvalidBirthDateError


class TestValidateBirthDate:
    @pytest.mark.parametrize("day, month, year", [
        ("15", "03", "1985"),
        ("01", "12", "1990"),
        ("31", "01", "2000"),
    ])
    def test_valid_date_passes(self, day, month, year):
        validate_birth_date(day, month, year)

    @pytest.mark.parametrize("day, month, year, expected_code", [
        ("6",  "06", "1990", InvalidBirthDateError.Code.INVALID_BIRTH_DAY_FORMAT),
        ("ab", "06", "1990", InvalidBirthDateError.Code.INVALID_BIRTH_DAY_FORMAT),
        ("06", "6",  "1990", InvalidBirthDateError.Code.INVALID_BIRTH_MONTH_FORMAT),
        ("06", "ab", "1990", InvalidBirthDateError.Code.INVALID_BIRTH_MONTH_FORMAT),
        ("06", "06", "90",   InvalidBirthDateError.Code.INVALID_BIRTH_YEAR_FORMAT),
        ("06", "06", "abc",  InvalidBirthDateError.Code.INVALID_BIRTH_YEAR_FORMAT),
    ])
    def test_invalid_date_raises(self, day, month, year, expected_code):
        with pytest.raises(InvalidBirthDateError) as exc_info:
            validate_birth_date(day, month, year)
        assert exc_info.value.code == expected_code
        assert exc_info.value.message is not None

    def test_day_error_message_describes_format(self):
        with pytest.raises(InvalidBirthDateError) as exc_info:
            validate_birth_date("6", "06", "1990")
        assert "2 dígitos" in exc_info.value.message

    def test_month_error_message_describes_format(self):
        with pytest.raises(InvalidBirthDateError) as exc_info:
            validate_birth_date("06", "6", "1990")
        assert "2 dígitos" in exc_info.value.message

    def test_year_error_message_describes_format(self):
        with pytest.raises(InvalidBirthDateError) as exc_info:
            validate_birth_date("06", "06", "97")
        assert "4 dígitos" in exc_info.value.message

    def test_error_string_format_day(self):
        with pytest.raises(InvalidBirthDateError) as exc_info:
            validate_birth_date("6", "06", "1990")
        assert "INVALID_BIRTH_DAY_FORMAT" in str(exc_info.value)

    def test_error_string_format_year(self):
        with pytest.raises(InvalidBirthDateError) as exc_info:
            validate_birth_date("06", "06", "97")
        assert "INVALID_BIRTH_YEAR_FORMAT" in str(exc_info.value)
