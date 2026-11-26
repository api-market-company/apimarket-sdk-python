"""
Tests de backward compatibility para los cambios entre main y develop (v4.6).
Verifica que el código escrito con la API vieja siga funcionando (con warnings).
"""
import warnings
import pytest
from apimarket.validations import (
    InvalidCURPError,
    InvalidNSSError,
    InvalidRFCError,
)


# ---------------------------------------------------------------------------
# InvalidCURPError
# ---------------------------------------------------------------------------

class TestInvalidCURPErrorBackwardCompat:
    def test_new_signature_no_warning(self):
        """La firma nueva (curp, code, message) no debe emitir ningún warning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            e = InvalidCURPError("XEXX010101MNEXXXA4", InvalidCURPError.Code.INVALID_FORMAT, "msg")
        assert len(w) == 0
        assert e.code == InvalidCURPError.Code.INVALID_FORMAT
        assert e.message == "msg"
        assert e.curp == "XEXX010101MNEXXXA4"

    def test_old_signature_emits_deprecation_warning(self):
        """La firma vieja (curp, message) debe funcionar y emitir DeprecationWarning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            e = InvalidCURPError("XEXX010101MNEXXXA4", "Invalid length.")
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert "deprecado" in str(w[0].message).lower()

    def test_old_signature_preserves_message(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            e = InvalidCURPError("X", "Invalid length.")
        assert e.message == "Invalid length."
        assert e.code is None
        assert e.curp == "X"

    def test_old_signature_str_format(self):
        """El __str__ sin code debe usar el formato antiguo (sin corchetes)."""
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            e = InvalidCURPError("X", "msg")
        assert str(e) == "CURP: X - msg"
        assert "[" not in str(e)

    def test_new_signature_str_format(self):
        """El __str__ con code debe mostrar el código entre corchetes."""
        e = InvalidCURPError("X", InvalidCURPError.Code.INVALID_LENGTH, "msg")
        assert "[INVALID_CURP_LENGTH]" in str(e)

    def test_old_signature_is_catchable(self):
        """El error con firma vieja debe seguir siendo catchable normalmente."""
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            with pytest.raises(InvalidCURPError):
                raise InvalidCURPError("X", "Invalid.")

    def test_old_signature_keyword_message(self):
        """Código viejo que usaba solo curp + mensaje posicional."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            e = InvalidCURPError("LOOA531113HTCPBN07", "CURP has invalid format.")
        assert e.message == "CURP has invalid format."
        assert issubclass(w[0].category, DeprecationWarning)


# ---------------------------------------------------------------------------
# InvalidNSSError
# ---------------------------------------------------------------------------

class TestInvalidNSSErrorBackwardCompat:
    def test_new_signature_no_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            e = InvalidNSSError("12345678901", InvalidNSSError.Code.INVALID_DIGIT, "msg")
        assert len(w) == 0
        assert e.code == InvalidNSSError.Code.INVALID_DIGIT

    def test_old_signature_emits_deprecation_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            e = InvalidNSSError("123", "Invalid length.")
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert e.code is None
        assert e.message == "Invalid length."

    def test_old_signature_str_no_brackets(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            e = InvalidNSSError("123", "Invalid length.")
        assert str(e) == "NSS: 123 - Invalid length."

    def test_new_signature_str_with_brackets(self):
        e = InvalidNSSError("123", InvalidNSSError.Code.INVALID_LENGTH, "msg")
        assert "[INVALID_NSS_LENGTH]" in str(e)


# ---------------------------------------------------------------------------
# InvalidRFCError
# ---------------------------------------------------------------------------

class TestInvalidRFCErrorBackwardCompat:
    def test_new_signature_no_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            e = InvalidRFCError("XAXX010101000", InvalidRFCError.Code.INVALID_FORMAT, "msg")
        assert len(w) == 0
        assert e.code == InvalidRFCError.Code.INVALID_FORMAT

    def test_old_signature_emits_deprecation_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            e = InvalidRFCError("XAXX", "Invalid RFC format.")
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert e.code is None
        assert e.message == "Invalid RFC format."

    def test_old_signature_str_no_brackets(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            e = InvalidRFCError("X", "msg")
        assert str(e) == "RFC: X - msg"
