import re

class InvalidCURPError(Exception):
    """Exception raised for invalid CURP."""

    def __init__(self, curp, message):
        self.curp = curp
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"CURP: {self.curp} - {self.message}"


class InvalidNSSError(Exception):
    """Exception raised for invalid NSS."""

    def __init__(self, nss, message):
        self.nss = nss
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"NSS: {self.nss} - {self.message}"


class InvalidRFCError(Exception):
    """Exception raised for invalid RFC."""

    def __init__(self, rfc, message):
        self.rfc = rfc
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"RFC: {self.rfc} - {self.message}"


def validate_rfc(rfc):
    """Validate the format of an RFC."""

    # RFC for individuals
    pattern_individual = r'^[A-Z]{4}[0-9]{6}[A-Z0-9]{3}$'

    # RFC for companies
    pattern_company = r'^[A-Z]{3}[0-9]{6}[A-Z0-9]{3}$'

    if not (re.match(pattern_individual, rfc) or re.match(pattern_company, rfc)):
        raise InvalidRFCError(rfc, "Invalid RFC format.")

    return rfc


def calculate_nss_verification_digit(nss):
    if len(nss) < 10:
        raise InvalidNSSError(nss, "Invalid length.")

    acc = 0
    for i in range(10):
        if i & 1:
            x = int(nss[i]) * 2
            acc += x % 10 + (1 if x >= 10 else 0)
        else:
            acc += int(nss[i])

    return str((10 - acc % 10) % 10)


def calculate_curp_verification_digit(curp17):
    """Calculate the check digit for a CURP."""
    diccionario = "0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    lngSuma = 0.0

    for i in range(17):
        lngSuma += diccionario.index(curp17[i]) * (18 - i)

    lngDigito = 10 - (lngSuma % 10)

    if lngDigito == 10:
        return '0'
    return str(int(lngDigito))


def validate_curp(curp):
    if len(curp) != 18:
        raise InvalidCURPError(curp, f"Invalid length {len(curp)}.")

    pattern = r'^[A-Z][AEIXOU][A-Z]{2}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HMX](AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[B-DF-HJ-NP-TV-Z]{3}[0-9A-Z][0-9]$'

    if not re.match(pattern, curp):
        raise InvalidCURPError(curp, f"CURP has invalid format.")

    digit = calculate_curp_verification_digit(curp[:17])
    if curp[17] != digit:
        raise InvalidCURPError(curp, f"CURP has an invalid check digit. It must be {digit}.")

    return curp


def validate_nss(nss):
    """Validate the format and check digit of an NSS."""
    # Check the length
    if len(nss) != 11:
        raise InvalidNSSError(nss, "Invalid length.")

    # Check if all characters are digits
    if not nss.isdigit():
        raise InvalidNSSError(nss, "Invalid format: NSS should only contain digits.")

    # Validate check digit
    if nss[10] != calculate_nss_verification_digit(nss[:10]):
        raise InvalidNSSError(nss, "Invalid check digit.")

    return nss
