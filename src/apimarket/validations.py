import re
import warnings
from enum import Enum

from apimarket.field_codes import FILE_CODES, PARAMETER_CODES

_MISSING = object()  # sentinel to distinguish old 2-arg from new 3-arg constructors

UUID_PATTERN = re.compile(
    r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
)


class ValidationError(ValueError):
    """Base de los errores detectados antes de llamar a la API.

    Todas sus subclases exponen ``code`` (miembro de un Enum) y ``message``.
    """


class InvalidFolioError(ValidationError):
    class Code(Enum):
        INVALID_FORMAT = "INVALID_FOLIO_FORMAT"

    def __init__(self, folio: str, code: Code, message: str):
        self.folio = folio
        self.code = code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"[{self.code.value}] Folio: {self.folio} - {self.message}"


class InvalidCURPError(ValidationError):
    class Code(Enum):
        INVALID_LENGTH = "INVALID_CURP_LENGTH"
        INVALID_FORMAT = "INVALID_CURP_FORMAT"
        INVALID_DIGIT  = "INVALID_CURP_DIGIT"

    def __init__(self, curp: str, code=_MISSING, message=_MISSING):
        if message is _MISSING:
            # Backward compat: old signature was (curp, message)
            warnings.warn(
                "InvalidCURPError(curp, message) está deprecado. "
                "Use InvalidCURPError(curp, InvalidCURPError.Code.X, message).",
                DeprecationWarning, stacklevel=2
            )
            self.curp = curp
            self.code = None
            self.message = code
        else:
            self.curp = curp
            self.code = code
            self.message = message
        super().__init__(self.message)

    def __str__(self):
        if self.code is None:
            return f"CURP: {self.curp} - {self.message}"
        return f"[{self.code.value}] CURP: {self.curp} - {self.message}"


class InvalidNSSError(ValidationError):
    class Code(Enum):
        INVALID_LENGTH = "INVALID_NSS_LENGTH"
        INVALID_FORMAT = "INVALID_NSS_FORMAT"
        INVALID_DIGIT  = "INVALID_NSS_DIGIT"

    def __init__(self, nss: str, code=_MISSING, message=_MISSING):
        if message is _MISSING:
            # Backward compat: old signature was (nss, message)
            warnings.warn(
                "InvalidNSSError(nss, message) está deprecado. "
                "Use InvalidNSSError(nss, InvalidNSSError.Code.X, message).",
                DeprecationWarning, stacklevel=2
            )
            self.nss = nss
            self.code = None
            self.message = code
        else:
            self.nss = nss
            self.code = code
            self.message = message
        super().__init__(self.message)

    def __str__(self):
        if self.code is None:
            return f"NSS: {self.nss} - {self.message}"
        return f"[{self.code.value}] NSS: {self.nss} - {self.message}"


class InvalidRFCError(ValidationError):
    class Code(Enum):
        INVALID_FORMAT = "INVALID_RFC_FORMAT"

    def __init__(self, rfc: str, code=_MISSING, message=_MISSING):
        if message is _MISSING:
            # Backward compat: old signature was (rfc, message)
            warnings.warn(
                "InvalidRFCError(rfc, message) está deprecado. "
                "Use InvalidRFCError(rfc, InvalidRFCError.Code.X, message).",
                DeprecationWarning, stacklevel=2
            )
            self.rfc = rfc
            self.code = None
            self.message = code
        else:
            self.rfc = rfc
            self.code = code
            self.message = message
        super().__init__(self.message)

    def __str__(self):
        if self.code is None:
            return f"RFC: {self.rfc} - {self.message}"
        return f"[{self.code.value}] RFC: {self.rfc} - {self.message}"


class InvalidBirthDateError(ValidationError):
    class Code(Enum):
        INVALID_BIRTH_DAY_FORMAT = "INVALID_BIRTH_DAY_FORMAT"
        INVALID_BIRTH_MONTH_FORMAT = "INVALID_BIRTH_MONTH_FORMAT"
        INVALID_BIRTH_YEAR_FORMAT = "INVALID_BIRTH_YEAR_FORMAT"

    def __init__(self, value: str, code: Code, message: str):
        self.value = value
        self.code = code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"[{self.code.value}] Value: {self.value} - {self.message}"


class InvalidCreditError(ValidationError):
    class Code(Enum):
        INVALID_FORMAT = "INVALID_CREDIT_FORMAT"

    def __init__(self, credit: str, code: Code, message: str):
        self.credit = credit
        self.code = code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"[{self.code.value}] Crédito: {self.credit} - {self.message}"


def validate_credit_number(credit):
    """Valida el formato de un número de crédito INFONAVIT."""
    if not re.fullmatch(r'[0-9]{10}', str(credit)):
        raise InvalidCreditError(str(credit), InvalidCreditError.Code.INVALID_FORMAT,
                                 "El número de crédito INFONAVIT debe contener exactamente 10 dígitos numéricos.")

    return credit


def code_token(parameter: str) -> str:
    """Nombre del parámetro dentro de un código: ``movimientos[0].apellidoPaterno`` → ``MOVIMIENTOS_APELLIDO_PATERNO``."""
    name = re.sub(r"\[\d+\]", "", parameter)
    name = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name)
    return re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_").upper()


def _field_codes(name: str, table: dict, qualified_name: str) -> Enum:
    """Un miembro ``<CAMPO>_<MOTIVO>`` con valor ``INVALID_<CAMPO>_<MOTIVO>``."""
    members = [(f"{field}_{reason}", f"INVALID_{field}_{reason}")
               for field, reasons in table.items() for reason in reasons.split()]
    return Enum(name, members, module=__name__, qualname=qualified_name)


class _FieldError(ValidationError):
    """Error de un parámetro; su código nombra el campo y el motivo."""

    def __init__(self, parameter: str, code: Enum, message: str):
        self.parameter = parameter
        self.code = code
        self.message = message
        super().__init__(self.message)

    @classmethod
    def of(cls, parameter: str, reason: str, message: str):
        return cls(parameter, cls.Code[f"{code_token(parameter)}_{reason}"], message)


class InvalidParameterError(_FieldError):
    Code = _field_codes("Code", PARAMETER_CODES, "InvalidParameterError.Code")

    def __str__(self):
        return f"[{self.code.value}] Parámetro: {self.parameter} - {self.message}"


class InvalidFileError(_FieldError):
    Code = _field_codes("Code", FILE_CODES, "InvalidFileError.Code")

    def __str__(self):
        return f"[{self.code.value}] Archivo: {self.parameter} - {self.message}"


class ConfigurationError(ValidationError):
    class Code(Enum):
        API_KEY_MISSING = "CONFIG_API_KEY_MISSING"
        IDSE_CREDENTIALS_MISSING = "CONFIG_IDSE_CREDENTIALS_MISSING"

    def __init__(self, code: Code, message: str):
        self.code = code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"[{self.code.value}] {self.message}"


def _require_text(value, parameter: str):
    if value is None:
        raise InvalidParameterError.of(parameter, "MISSING", f"El parámetro '{parameter}' es obligatorio.")
    if not isinstance(value, str):
        raise InvalidParameterError.of(parameter, "TYPE", f"El parámetro '{parameter}' debe ser texto.")


def validate_birth_date(day, month, year):
    day_str, month_str, year_str = str(day), str(month), str(year)
    if not day_str.isdigit() or len(day_str) != 2:
        raise InvalidBirthDateError(day_str, InvalidBirthDateError.Code.INVALID_BIRTH_DAY_FORMAT,
                                    "El día de nacimiento debe tener exactamente 2 dígitos (ej. '06').")
    if not month_str.isdigit() or len(month_str) != 2:
        raise InvalidBirthDateError(month_str, InvalidBirthDateError.Code.INVALID_BIRTH_MONTH_FORMAT,
                                    "El mes de nacimiento debe tener exactamente 2 dígitos (ej. '06').")
    if not year_str.isdigit() or len(year_str) != 4:
        raise InvalidBirthDateError(year_str, InvalidBirthDateError.Code.INVALID_BIRTH_YEAR_FORMAT,
                                    "El año de nacimiento debe tener exactamente 4 dígitos (ej. '1990').")


def validate_folio_uuid(folio: str) -> str:
    _require_text(folio, "folio")
    if not UUID_PATTERN.match(folio):
        raise InvalidFolioError(folio, InvalidFolioError.Code.INVALID_FORMAT, "El folio debe tener formato UUID válido (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx).")
    return folio


def validate_rfc(rfc):
    _require_text(rfc, "rfc")
    pattern_individual = r'^[A-Z]{4}[0-9]{6}[A-Z0-9]{3}$'
    pattern_company    = r'^[A-Z]{3}[0-9]{6}[A-Z0-9]{3}$'

    if not (re.match(pattern_individual, rfc) or re.match(pattern_company, rfc)):
        raise InvalidRFCError(rfc, InvalidRFCError.Code.INVALID_FORMAT, "Formato de RFC inválido.")

    return rfc


def calculate_nss_verification_digit(nss):
    if len(nss) < 10:
        raise InvalidNSSError(nss, InvalidNSSError.Code.INVALID_LENGTH, "Longitud inválida.")

    acc = 0
    for i in range(10):
        if i & 1:
            x = int(nss[i]) * 2
            acc += x % 10 + (1 if x >= 10 else 0)
        else:
            acc += int(nss[i])

    return str((10 - acc % 10) % 10)


def calculate_curp_verification_digit(curp17):
    dictionary = "0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    checksum = 0.0

    for i in range(17):
        checksum += dictionary.index(curp17[i]) * (18 - i)

    digit = 10 - (checksum % 10)

    if digit == 10:
        return '0'
    return str(int(digit))


def validate_curp(curp):
    _require_text(curp, "curp")
    if len(curp) != 18:
        raise InvalidCURPError(curp, InvalidCURPError.Code.INVALID_LENGTH, f"Longitud inválida: se esperaban 18 caracteres, se recibieron {len(curp)}.")

    pattern = r'^[A-Z][AEIXOU][A-Z]{2}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HMX](AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[B-DF-HJ-NP-TV-Z]{3}[0-9A-Z][0-9]$'

    if not re.match(pattern, curp):
        raise InvalidCURPError(curp, InvalidCURPError.Code.INVALID_FORMAT, "El formato del CURP es inválido.")

    digit = calculate_curp_verification_digit(curp[:17])
    if curp[17] != digit:
        raise InvalidCURPError(curp, InvalidCURPError.Code.INVALID_DIGIT, "Dígito verificador inválido.")

    return curp


def validate_nss(nss):
    _require_text(nss, "nss")
    if len(nss) != 11:
        raise InvalidNSSError(nss, InvalidNSSError.Code.INVALID_LENGTH, f"Longitud inválida: se esperaban 11 dígitos, se recibieron {len(nss)}.")

    if not nss.isdigit():
        raise InvalidNSSError(nss, InvalidNSSError.Code.INVALID_FORMAT, "El NSS solo debe contener dígitos.")

    if nss[10] != calculate_nss_verification_digit(nss[:10]):
        raise InvalidNSSError(nss, InvalidNSSError.Code.INVALID_DIGIT, "Dígito verificador inválido.")

    return nss
