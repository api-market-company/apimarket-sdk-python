"""Un escenario real por cada código de error. Lo usan las pruebas y ``tests/ver_errores.py``."""
import contextlib
import io
import json
from dataclasses import dataclass
from typing import Callable

import httpx
from kink import di

import apimarket
import fuzz
from apimarket import rules
from apimarket.api_market_client import ApiMarketClient
from apimarket.cli import main
from apimarket.errors import ErrorCode
from apimarket.validations import (ConfigurationError, InvalidBirthDateError, InvalidCreditError, InvalidCURPError,
                                   InvalidFileError, InvalidFolioError, InvalidNSSError, InvalidParameterError,
                                   InvalidRFCError)

from arguments import VALID

CURP, NSS, UUID = "XEXX010101MNEXXXA4", "12345678903", "550e8400-e29b-41d4-a716-446655440000"
PERSON = ("JUAN", "PEREZ", "LOPEZ")


@dataclass(frozen=True)
class Scenario:
    code: object
    description: str
    call: Callable
    setup: Callable = lambda server: None
    sends_request: bool = False


def local(code, description, call, setup=lambda server: None):
    return Scenario(code, description, call, setup)


def reply(status, message, body_status=None):
    def setup(server):
        payload = {"success": False, "codigoValidacion": "EJEMPLO123", "message": message,
                   "status": body_status or status}
        server.reply = (status, "application/json", json.dumps(payload, ensure_ascii=False).encode())

    return setup


def api(code, status, message, description):
    # read_sat_message no se reintenta, así que 429 y 503 responden de inmediato.
    return Scenario(code, description, lambda: apimarket.read_sat_message("u1"), reply(status, message),
                    sends_request=True)


def broken_response(server):
    server.reply = (200, "application/json", b"{roto")


def unreachable(server):
    di[ApiMarketClient].request_adapter.base_url = "http://127.0.0.1:1"


def slow(server):
    server.delay = 0.5
    di[ApiMarketClient].request_adapter._http_client.timeout = httpx.Timeout(0.1)


def without_api_key(server):
    di["API_MARKET_API_KEY"] = ""


def without_idse_credentials(server):
    di["IDSEPRO_BEARER_TOKEN"] = ""


class CommandError(Exception):
    """Salida de la CLI convertida en excepción para mostrarla igual que las demás."""

    def __init__(self, code, message, exit_status):
        super().__init__(message)
        self.code, self.message, self.exit_status = code, message, exit_status


def command(*argv):
    def call():
        stderr = io.StringIO()
        try:
            with contextlib.redirect_stderr(stderr):
                main(list(argv))
        except SystemExit as exit_:
            line = stderr.getvalue().strip().splitlines()[-1]
            code, message = line.split("]: ", 1)
            raise CommandError(ErrorCode(code.removeprefix("Error [")), message, exit_.code)

    return call


def large_template():
    """El límite real es de 500 MB; aquí se baja para no crear un archivo de ese tamaño."""
    original = rules.TEMPLATE_MAX_MEGABYTES
    rules.TEMPLATE_MAX_MEGABYTES = 1
    try:
        apimarket.create_template(b" " * (2 * 1024 * 1024))
    finally:
        rules.TEMPLATE_MAX_MEGABYTES = original


def _short(value):
    text = repr(value)
    return text if len(text) <= 60 else text[:57] + "..."


def _field_scenarios():
    """Un caso por cada código de parámetro o archivo, encontrado al recorrer todas las funciones."""
    found, _ = fuzz.run()
    for code, (name, changes, _error) in sorted(found.items(), key=lambda item: item[0].value):
        if isinstance(code, (InvalidParameterError.Code, InvalidFileError.Code)):
            def call(name=name, changes=changes):
                return getattr(apimarket, name)(**{**VALID[name], **changes})

            yield local(code, f"{name}({', '.join(f'{k}={_short(v)}' for k, v in changes.items())})", call)
    yield local(InvalidFileError.Code.TEMPLATE_FILE_SIZE, "Plantilla que supera el tamaño máximo", large_template)


_curp, _rfc, _nss = InvalidCURPError.Code, InvalidRFCError.Code, InvalidNSSError.Code
_date = InvalidBirthDateError.Code

SCENARIOS = [
    local(_curp.INVALID_LENGTH, "CURP corta", lambda: apimarket.fetch_curp_details("CORTA")),
    local(_curp.INVALID_FORMAT, "CURP solo con dígitos",
          lambda: apimarket.fetch_curp_details("123456789012345678")),
    local(_curp.INVALID_DIGIT, "CURP con dígito verificador malo",
          lambda: apimarket.fetch_curp_details("XEXX010101MNEXXXA9")),
    local(_rfc.INVALID_FORMAT, "RFC mal formado", lambda: apimarket.check_sat_rfc("MAL")),
    local(_nss.INVALID_LENGTH, "NSS corto", lambda: apimarket.get_assigned_umf("123")),
    local(_nss.INVALID_FORMAT, "NSS con letras", lambda: apimarket.get_assigned_umf("1234567890A")),
    local(_nss.INVALID_DIGIT, "NSS con dígito verificador malo", lambda: apimarket.get_assigned_umf("12345678900")),
    local(_date.INVALID_BIRTH_DAY_FORMAT, "Día de un dígito",
          lambda: apimarket.calculate_rfc(*PERSON, "1", "01", "1990")),
    local(_date.INVALID_BIRTH_MONTH_FORMAT, "Mes de un dígito",
          lambda: apimarket.calculate_rfc(*PERSON, "01", "1", "1990")),
    local(_date.INVALID_BIRTH_YEAR_FORMAT, "Año de dos dígitos",
          lambda: apimarket.calculate_rfc(*PERSON, "01", "01", "90")),
    local(InvalidFolioError.Code.INVALID_FORMAT, "Folio que no es UUID",
          lambda: apimarket.validate_sep_certificate("FOLIO123")),
    local(InvalidCreditError.Code.INVALID_FORMAT, "Crédito con 3 dígitos",
          lambda: apimarket.get_infonavit_credit_history("123")),
    local(ConfigurationError.Code.API_KEY_MISSING, "Sin llave", apimarket.get_balance, without_api_key),
    local(ConfigurationError.Code.IDSE_CREDENTIALS_MISSING, "Sin credenciales de IDSE Pro",
          apimarket.idse_list_certificates, without_idse_credentials),
    api(ErrorCode.API_REQUEST_INVALID, 400, "Error de validacion", "La API responde 400"),
    api(ErrorCode.API_KEY_UNAUTHORIZED, 401, "El token proporcionado no es valido.", "La API responde 401"),
    api(ErrorCode.API_PAYMENT_REQUIRED, 402, "Requiere un paquete Business.", "La API responde 402"),
    api(ErrorCode.API_PERMISSION_FORBIDDEN, 403, "No tienes permiso.", "La API responde 403"),
    api(ErrorCode.API_RESOURCE_NOT_FOUND, 404, "Esta ruta no existe", "La API responde 404"),
    api(ErrorCode.API_REQUEST_UNPROCESSABLE, 422, "error de validacion", "La API responde 422"),
    api(ErrorCode.API_REQUEST_LIMIT_EXCEEDED, 429, "Demasiadas solicitudes.", "La API responde 429"),
    api(ErrorCode.API_REQUEST_FAILED, 409, "Conflicto.", "La API responde otro 4xx"),
    api(ErrorCode.API_SERVER_ERROR, 500, "Error desconocido.", "La API responde 500"),
    api(ErrorCode.API_SERVICE_UNAVAILABLE, 503, "En mantenimiento.", "La API responde 503"),
    Scenario(ErrorCode.API_RESPONSE_INVALID, "JSON ilegible", apimarket.get_balance, broken_response, True),
    Scenario(ErrorCode.NETWORK_CONNECTION_ERROR, "Servidor inaccesible", apimarket.get_balance, unreachable),
    Scenario(ErrorCode.NETWORK_RESPONSE_TIMEOUT, "La API tarda demasiado", apimarket.get_balance, slow, True),
    local(ErrorCode.CLI_ARGUMENTS_INVALID, "Comando sin un argumento obligatorio", command("sat", "declaraciones")),
]

SCENARIOS += _field_scenarios()
