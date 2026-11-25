"""Códigos de error del SDK y su catálogo.

Toda excepción que entrega el SDK lleva un atributo ``code``:

* validación local: subclases de :class:`apimarket.validations.ValidationError`;
* respuestas de la API: ``APIError`` (incluida ``ApiMarketError``);
* fallas de red: las excepciones de ``httpx``.
"""
from enum import Enum

import httpx
from kiota_abstractions.api_error import APIError

from apimarket import validations as v


class ErrorCode(Enum):
    """Errores que no provienen de una validación local."""
    API_REQUEST_INVALID = "API_REQUEST_INVALID"
    API_KEY_UNAUTHORIZED = "API_KEY_UNAUTHORIZED"
    API_PAYMENT_REQUIRED = "API_PAYMENT_REQUIRED"
    API_PERMISSION_FORBIDDEN = "API_PERMISSION_FORBIDDEN"
    API_RESOURCE_NOT_FOUND = "API_RESOURCE_NOT_FOUND"
    API_REQUEST_UNPROCESSABLE = "API_REQUEST_UNPROCESSABLE"
    API_REQUEST_LIMIT_EXCEEDED = "API_REQUEST_LIMIT_EXCEEDED"
    API_REQUEST_FAILED = "API_REQUEST_FAILED"
    API_SERVER_ERROR = "API_SERVER_ERROR"
    API_SERVICE_UNAVAILABLE = "API_SERVICE_UNAVAILABLE"
    API_RESPONSE_INVALID = "API_RESPONSE_INVALID"
    NETWORK_CONNECTION_ERROR = "NETWORK_CONNECTION_ERROR"
    NETWORK_RESPONSE_TIMEOUT = "NETWORK_RESPONSE_TIMEOUT"
    CLI_ARGUMENTS_INVALID = "CLI_ARGUMENTS_INVALID"


_BY_STATUS = {
    400: ErrorCode.API_REQUEST_INVALID,
    401: ErrorCode.API_KEY_UNAUTHORIZED,
    402: ErrorCode.API_PAYMENT_REQUIRED,
    403: ErrorCode.API_PERMISSION_FORBIDDEN,
    404: ErrorCode.API_RESOURCE_NOT_FOUND,
    422: ErrorCode.API_REQUEST_UNPROCESSABLE,
    429: ErrorCode.API_REQUEST_LIMIT_EXCEEDED,
    502: ErrorCode.API_SERVICE_UNAVAILABLE,
    503: ErrorCode.API_SERVICE_UNAVAILABLE,
    504: ErrorCode.API_SERVICE_UNAVAILABLE,
}


def api_error_code(status) -> ErrorCode:
    """Código que corresponde a un estado HTTP de error."""
    if status in _BY_STATUS:
        return _BY_STATUS[status]
    if isinstance(status, int) and 400 <= status < 500:
        return ErrorCode.API_REQUEST_FAILED
    return ErrorCode.API_SERVER_ERROR


def annotate(error: BaseException) -> None:
    """Agrega ``code`` (y ``message`` a los de red) sin cambiar el tipo del error."""
    if getattr(error, "code", None) is not None and isinstance(getattr(error, "code"), ErrorCode):
        return
    if isinstance(error, APIError):
        error.code = api_error_code(error.response_status_code)
    elif isinstance(error, httpx.TimeoutException):
        error.code = ErrorCode.NETWORK_RESPONSE_TIMEOUT
        error.message = "La API no respondió a tiempo."
    elif isinstance(error, httpx.HTTPError):
        error.code = ErrorCode.NETWORK_CONNECTION_ERROR
        detail = f" ({error})" if str(error) else ""
        error.message = f"No fue posible conectar con la API{detail}."


_REASONS = {
    "MISSING": "Falta '{field}' o llegó vacío.",
    "TYPE": "'{field}' no tiene el tipo de dato esperado.",
    "LENGTH": "La longitud o cantidad de '{field}' está fuera de los límites.",
    "RANGE": "El valor de '{field}' está fuera del rango permitido.",
    "FORMAT": "'{field}' no tiene el formato esperado.",
    "OPTION": "'{field}' no está entre las opciones permitidas.",
    "COMBINATION": "'{field}' no es compatible con los demás parámetros.",
    "PATH": "'{field}' forma parte de la URL y no puede ser '.' ni '..'.",
    "FILE_NOT_FOUND": "No existe el archivo indicado en '{field}'.",
    "FILE_UNREADABLE": "No se puede leer el archivo de '{field}'.",
    "FILE_EMPTY": "El archivo de '{field}' está vacío.",
    "FILE_TYPE": "El tipo del archivo de '{field}' no está permitido.",
    "FILE_SIZE": "El archivo de '{field}' supera el tamaño máximo.",
    "FILE_CONTENT": "El contenido del archivo de '{field}' no es válido.",
}


def _field_entries(codes):
    entries = []
    for code in codes:
        # El motivo es el sufijo más largo conocido: CSF_FILE_TYPE → FILE_TYPE.
        reason = max((r for r in _REASONS if code.name.endswith("_" + r)), key=len)
        entries.append((code, _REASONS[reason].format(field=code.name[:-len(reason) - 1].lower())))
    return entries


#: (título, excepción, [(miembro del Enum, descripción)])
CATALOG = [
    ("CURP", "InvalidCURPError", [
        (v.InvalidCURPError.Code.INVALID_LENGTH, "La CURP no tiene exactamente 18 caracteres."),
        (v.InvalidCURPError.Code.INVALID_FORMAT, "La CURP no cumple el patrón oficial."),
        (v.InvalidCURPError.Code.INVALID_DIGIT, "El dígito verificador de la CURP no corresponde."),
    ]),
    ("RFC", "InvalidRFCError", [
        (v.InvalidRFCError.Code.INVALID_FORMAT, "El RFC no cumple el patrón de persona física o moral, en mayúsculas."),
    ]),
    ("NSS", "InvalidNSSError", [
        (v.InvalidNSSError.Code.INVALID_LENGTH, "El NSS no tiene exactamente 11 dígitos."),
        (v.InvalidNSSError.Code.INVALID_FORMAT, "El NSS contiene caracteres no numéricos."),
        (v.InvalidNSSError.Code.INVALID_DIGIT, "El dígito verificador del NSS no corresponde."),
    ]),
    ("Fecha de nacimiento", "InvalidBirthDateError", [
        (v.InvalidBirthDateError.Code.INVALID_BIRTH_DAY_FORMAT, "El día no tiene exactamente 2 dígitos."),
        (v.InvalidBirthDateError.Code.INVALID_BIRTH_MONTH_FORMAT, "El mes no tiene exactamente 2 dígitos."),
        (v.InvalidBirthDateError.Code.INVALID_BIRTH_YEAR_FORMAT, "El año no tiene exactamente 4 dígitos."),
    ]),
    ("Folio de certificado", "InvalidFolioError", [
        (v.InvalidFolioError.Code.INVALID_FORMAT, "El folio no es un UUID."),
    ]),
    ("Número de crédito INFONAVIT", "InvalidCreditError", [
        (v.InvalidCreditError.Code.INVALID_FORMAT, "El número de crédito no tiene exactamente 10 dígitos."),
    ]),
    ("Parámetros", "InvalidParameterError", _field_entries(v.InvalidParameterError.Code)),
    ("Archivos", "InvalidFileError", _field_entries(v.InvalidFileError.Code)),
    ("Configuración", "ConfigurationError", [
        (v.ConfigurationError.Code.API_KEY_MISSING, "No se configuró la llave de API Market."),
        (v.ConfigurationError.Code.IDSE_CREDENTIALS_MISSING, "No se configuraron las credenciales de IDSE Pro."),
    ]),
    ("Respuestas de la API", "APIError", [
        (ErrorCode.API_REQUEST_INVALID, "HTTP 400: la API rechazó la solicitud."),
        (ErrorCode.API_KEY_UNAUTHORIZED, "HTTP 401: la llave no es válida."),
        (ErrorCode.API_PAYMENT_REQUIRED, "HTTP 402: se requiere saldo o un paquete superior."),
        (ErrorCode.API_PERMISSION_FORBIDDEN, "HTTP 403: la llave no tiene permiso para el servicio."),
        (ErrorCode.API_RESOURCE_NOT_FOUND, "HTTP 404: no se encontró el recurso."),
        (ErrorCode.API_REQUEST_UNPROCESSABLE, "HTTP 422: la API no aceptó los datos."),
        (ErrorCode.API_REQUEST_LIMIT_EXCEEDED, "HTTP 429: demasiadas solicitudes."),
        (ErrorCode.API_REQUEST_FAILED, "Otro error HTTP 4xx."),
        (ErrorCode.API_SERVER_ERROR, "Error HTTP 5xx."),
        (ErrorCode.API_SERVICE_UNAVAILABLE, "HTTP 502, 503 o 504: el servicio no está disponible."),
        (ErrorCode.API_RESPONSE_INVALID, "La API respondió algo que no se puede interpretar."),
    ]),
    ("Red", "httpx.HTTPError", [
        (ErrorCode.NETWORK_CONNECTION_ERROR, "No fue posible conectar con la API."),
        (ErrorCode.NETWORK_RESPONSE_TIMEOUT, "La API no respondió a tiempo."),
    ]),
    ("Línea de comandos", "CLI", [
        (ErrorCode.CLI_ARGUMENTS_INVALID, "Faltan argumentos o tienen un tipo incorrecto."),
    ]),
]
