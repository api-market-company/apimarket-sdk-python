import asyncio
import copy
import inspect
import json
import os
import sys
import threading
import warnings
from asyncio import Future
from dataclasses import make_dataclass
from typing import Union

from decouple import config
from kink import inject, di
from kiota_abstractions.authentication import AccessTokenProvider, AllowedHostsValidator, \
    BaseBearerTokenAuthenticationProvider
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_abstractions.headers_collection import HeadersCollection
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from kiota_http.kiota_client_factory import KiotaClientFactory
from kiota_serialization_json.json_serialization_writer import JsonSerializationWriter

from apimarket.api.imss.grupo.historial_laboral.historial_laboral_post_response import HistorialLaboralPostResponse
from apimarket.api.infonavit.grupo.buscar_credito.buscar_credito_post_response import BuscarCreditoPostResponse
from apimarket.api.infonavit.grupo.obtener_cuenta.obtener_cuenta_post_response import ObtenerCuentaPostResponse
from apimarket.api.renapo.grupo.buscar_nacimiento.buscar_nacimiento_post_response import BuscarNacimientoPostResponse
from apimarket.api.renapo.grupo.obtener_curp.obtener_curp_post_response import ObtenerCurpPostResponse
from apimarket.api.sat.grupo.calcular_rfc.calcular_rfc_post_response import CalcularRfcPostResponse
from apimarket.api.sat.grupo.obtener_datos.obtener_datos_post_response import ObtenerDatosPostResponse
from apimarket.api.sat.grupo.obtener_rfc.obtener_rfc_post_response import ObtenerRfcPostResponse
from apimarket.api.sat.grupo.validar_datos.validar_datos_post_response import ValidarDatosPostResponse
from apimarket.api.sat.v2.lista69b.lista69b_post_response import Lista69bPostResponse
from apimarket.api.sep.grupo.obtener_cedula.obtener_cedula_post_response import ObtenerCedulaPostResponse
from apimarket.api.sep.grupo.validar_cedula.validar_cedula_post_response import ValidarCedulaPostResponse
from apimarket.api.sep.grupo.validar_certificado.validar_certificado_get_response import ValidarCertificadoGetResponse
# Backward compat: the old class name is kept as a deprecated alias
from apimarket.api.sep.grupo.validar_certificado import validar_certificado_post_response as _vcp_mod
ValidarCertificadoPostResponse = ValidarCertificadoGetResponse  # same object, warning fires on direct module import
from apimarket.api_market_client import ApiMarketClient
from apimarket.models.curp_a_p_i_response import CurpAPIResponse
from apimarket.models.historial_data import HistorialData
from apimarket import rules
from apimarket.errors import ErrorCode, annotate
from apimarket.validations import (validate_curp, validate_rfc, validate_nss, validate_folio_uuid, validate_birth_date,
                                   ValidationError, ConfigurationError, InvalidParameterError, InvalidFileError,
                                   InvalidCURPError, InvalidRFCError, InvalidNSSError, InvalidFolioError,
                                   InvalidBirthDateError, InvalidCreditError)

# Workaround: Python 3.14 changed asyncio.current_task() behavior, breaking
# sniffio's asyncio detection. Fall back to get_running_loop() which still works.
if sys.version_info >= (3, 14):
    import sniffio as _sniffio
    import sniffio._impl as _sniffio_impl
    _original_sniffio_detect = _sniffio_impl.current_async_library

    def _patched_sniffio_detect():
        try:
            return _original_sniffio_detect()
        except _sniffio_impl.AsyncLibraryNotFoundError:
            import asyncio as _asyncio
            try:
                _asyncio.get_running_loop()
                return "asyncio"
            except RuntimeError:
                pass
            raise

    _sniffio.current_async_library = _patched_sniffio_detect
    _sniffio_impl.current_async_library = _patched_sniffio_detect

class EnvironmentTokenProvider(AccessTokenProvider):
    def __init__(self, token=""):
        self.token = token

    async def get_authorization_token(self, uri: str, additional_authentication_context=None) -> str:
        if additional_authentication_context is None:
            additional_authentication_context = {}
        return self.token

    def get_allowed_hosts_validator(self) -> AllowedHostsValidator:
        pass


def assemble(api_key: str = "", headers: dict[str, str] = None, sandbox: bool = False, async_client: bool = False, idse_pro_bearer_token: str = "", idse_pro_api_key: str = ""):
    if headers is None:
        headers = {}
    collection = HeadersCollection()
    collection.try_add("Accept", "application/json")
    sandbox = config("APIMARKET_SANDBOX", default=sandbox, cast=bool)
    if sandbox:
        collection.add("x-sandbox", "true")
    for k, v in headers.items():
        collection.add(k, v)
    di["async_client"] = async_client
    di["API_MARKET_API_KEY"] = config("APIMARKET_API_KEY", default=api_key)
    di["IDSEPRO_BEARER_TOKEN"] = config("IDSEPRO_BEARER_TOKEN", default=idse_pro_bearer_token)
    di["IDSEPRO_API_KEY"] = config("IDSEPRO_API_KEY", default=idse_pro_api_key)
    di[EnvironmentTokenProvider] = lambda di: EnvironmentTokenProvider(di["API_MARKET_API_KEY"])
    di[AccessTokenProvider] = lambda di: BaseBearerTokenAuthenticationProvider(di[EnvironmentTokenProvider])
    di[RequestAdapter] = lambda di: HttpxRequestAdapter(
        di[AccessTokenProvider],
        http_client=KiotaClientFactory.create_with_default_middleware()
    )
    di[ApiMarketClient] = lambda di: ApiMarketClient(di[RequestAdapter])
    di[HeadersCollection] = collection
    di[RequestConfiguration] = lambda di: RequestConfiguration(headers=di[HeadersCollection])
    return di


assemble()

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError


def make_query_params(params: dict):
    return make_dataclass('QueryParams', [(key, str) for key in params.keys()])(**params)


_sync_loop = None
_sync_loop_pid = None
_sync_loop_lock = threading.Lock()


def get_sync_event_loop():
    """Bucle de eventos de las llamadas síncronas, en un hilo propio.

    El cliente HTTP reutiliza conexiones, así que todas las llamadas deben correr
    en el mismo bucle. También permite llamar desde un bucle activo (Jupyter).
    """
    global _sync_loop, _sync_loop_pid
    with _sync_loop_lock:
        # Tras un fork() el hilo no existe en el proceso hijo.
        if _sync_loop is None or _sync_loop_pid != os.getpid():
            _sync_loop = asyncio.new_event_loop()
            _sync_loop_pid = os.getpid()
            threading.Thread(target=_sync_loop.run_forever, name="apimarket-sync", daemon=True).start()
        return _sync_loop


def ensure_api_key():
    """Evita enviar una petición sin llave."""
    if not di["API_MARKET_API_KEY"]:
        raise ConfigurationError(ConfigurationError.Code.API_KEY_MISSING,
                                 "Configure APIMARKET_API_KEY o llame a assemble(api_key=...).")


def choice_process_scheduler(func):
    def wrapper(*args, **kwargs):
        async def _coro():
            try:
                return await func(*args, **kwargs)
            except Exception as error:
                annotate(error)  # agrega error.code sin cambiar el tipo
                raise

        if di["async_client"]:
            return _coro()

        future = asyncio.run_coroutine_threadsafe(_coro(), get_sync_event_loop())
        try:
            return future.result()
        except BaseException:
            future.cancel()
            raise

    return wrapper


def format_api(func):
    def wrapper(*args, **kwargs):
        func_signature = inspect.signature(func)
        bound_arguments = func_signature.bind(*args, **kwargs)
        bound_arguments.apply_defaults()
        arguments = bound_arguments.arguments

        api, configuration = func(*args, **kwargs)
        ensure_api_key()

        # La configuración inyectada es compartida y la petición se arma después,
        # al ejecutar la corrutina: cada llamada necesita su propia copia.
        request_configuration = copy.copy(configuration)
        request_configuration.query_parameters = make_query_params(arguments)

        return choice_process_scheduler(lambda: api(request_configuration=request_configuration))()

    # Parameter names in @format_api-decorated functions must match the API's
    # query parameter names exactly (camelCase). Renaming them to snake_case
    # would break the HTTP request since names are extracted via inspect.signature.
    return wrapper


def to_json(response):
    if response is None or isinstance(response, (dict, list)):
        return json.dumps(response, ensure_ascii=False, default=str)
    json_serialization_writer = JsonSerializationWriter()
    response.serialize(json_serialization_writer)
    content = json_serialization_writer.get_serialized_content()
    return content.decode("utf-8")


@format_api
@inject()
def fetch_curp_details(curp: str, client: ApiMarketClient = None, configuration: RequestConfiguration = None) -> Union[
    Future[CurpAPIResponse], CurpAPIResponse]:
    validate_curp(curp)
    return client.api.renapo.grupo.valida_curp.post, configuration


@format_api
@inject()
def get_birth_record(curp: str, client: ApiMarketClient = None, configuration: RequestConfiguration = None) -> Union[
    Future[BuscarNacimientoPostResponse], BuscarNacimientoPostResponse]:
    validate_curp(curp)
    return client.api.renapo.grupo.buscar_nacimiento.post, configuration


@format_api
@inject()
def get_curp_from_details(nombres: str, paterno: str, materno: str, diaNacimiento: int, mesNacimiento: int,
                          anoNacimiento: int, claveEntidad: str, sexo: str, client: ApiMarketClient = None,
                          configuration: RequestConfiguration = None) -> Union[
    Future[ObtenerCurpPostResponse], ObtenerCurpPostResponse]:
    rules.text("nombres", nombres)
    rules.text("paterno", paterno)
    if materno != "":
        rules.optional_text("materno", materno)
    validate_birth_date(diaNacimiento, mesNacimiento, anoNacimiento)
    rules.option("claveEntidad", claveEntidad, rules.ENTITIES, ignore_case=True)
    rules.option("sexo", sexo, ("H", "M", "X"))
    return client.api.renapo.grupo.obtener_curp.post, configuration


@format_api
@inject()
def get_rfc_from_curp(curp: str, client: ApiMarketClient = None, configuration: RequestConfiguration = None) -> Union[
    Future[ObtenerRfcPostResponse], ObtenerRfcPostResponse]:
    validate_curp(curp)
    return client.api.sat.grupo.obtener_rfc.post, configuration


@format_api
@inject()
def _calculate_rfc(nombres: str, paterno: str, materno: str, diaNacimiento: str, mesNacimiento: str, anoNacimiento: str,
                   client: ApiMarketClient = None, configuration: RequestConfiguration = None) -> Union[
    Future[CalcularRfcPostResponse], CalcularRfcPostResponse]:
    rules.text("nombres", nombres)
    rules.text("paterno", paterno)
    if materno != "":
        rules.optional_text("materno", materno)
    validate_birth_date(diaNacimiento, mesNacimiento, anoNacimiento)
    return client.api.sat.grupo.calcular_rfc.post, configuration


def calculate_rfc(nombres: str, paterno: str, materno: str, diaNacimiento, mesNacimiento, anoNacimiento, **kwargs):
    """Calcula RFC. Acepta fechas como str ('06') o como int (deprecado)."""
    if isinstance(diaNacimiento, int):
        warnings.warn(
            "calculate_rfc() con fechas como int (ej. 6) está deprecado. "
            "Use strings con cero al inicio: diaNacimiento='01', mesNacimiento='01', anoNacimiento='1990'.",
            DeprecationWarning, stacklevel=2
        )
        # Los valores que no son int pasan sin cambios y los revisa la validación.
        diaNacimiento = f"{diaNacimiento:02d}"
        mesNacimiento = f"{mesNacimiento:02d}" if isinstance(mesNacimiento, int) else mesNacimiento
        anoNacimiento = str(anoNacimiento)
    return _calculate_rfc(nombres, paterno, materno, diaNacimiento, mesNacimiento, anoNacimiento, **kwargs)


@format_api
@inject()
def locate_umf_by_cp(cp: str, client: ApiMarketClient = None, configuration: RequestConfiguration = None):
    rules.digits("cp", cp, 5, 5)
    return client.api.imss.grupo.localizar_umf.post, configuration


@format_api
@inject()
def locate_nss_by_curp(curp: str, client: ApiMarketClient = None, configuration: RequestConfiguration = None):
    validate_curp(curp)
    return client.api.imss.grupo.localizar_nss.post, configuration


@format_api
@inject()
def check_nss_validity(nss: str, curp: str, client: ApiMarketClient = None, configuration: RequestConfiguration = None):
    validate_curp(curp)
    validate_nss(nss)
    return client.api.imss.grupo.consultar_vigencia.post, configuration


@format_api
@inject()
def get_clinic_by_curp(curp: str, client: ApiMarketClient = None, configuration: RequestConfiguration = None):
    validate_curp(curp)
    return client.api.imss.grupo.con_clinica.post, configuration


@format_api
@inject()
def consult_clinic_by_curp(curp: str, client: ApiMarketClient = None, configuration: RequestConfiguration = None):
    validate_curp(curp)
    return client.api.imss.grupo.con_clinica.post, configuration


@format_api
@inject()
def get_labor_history(curp: str, nss: str, client: ApiMarketClient = None,
                      configuration: RequestConfiguration = None) -> Union[Future[HistorialData], HistorialData]:
    validate_curp(curp)
    validate_nss(nss)
    return client.api.imss.grupo.historial_laboral.post, configuration


@format_api
@inject()
def validate_sep_cedula(cedula: str, client: ApiMarketClient = None, configuration: RequestConfiguration = None) -> \
        Union[Future[ValidarCedulaPostResponse], ValidarCedulaPostResponse]:
    rules.digits("cedula", cedula, 1, 10)
    return client.api.sep.grupo.validar_cedula.post, configuration


@format_api
@inject()
def validate_sep_certificate(folio: str, client: ApiMarketClient = None, configuration: RequestConfiguration = None) -> \
        Union[Future[ValidarCertificadoGetResponse], ValidarCertificadoGetResponse]:
    validate_folio_uuid(folio)
    return client.api.sep.grupo.validar_certificado.post, configuration


@format_api
@inject()
def _obtain_sep_cedula(curp: str, client: ApiMarketClient = None,
                       configuration: RequestConfiguration = None) -> Union[
    Future[ObtenerCedulaPostResponse], ObtenerCedulaPostResponse]:
    validate_curp(curp)
    return client.api.sep.grupo.obtener_cedula.post, configuration


def obtain_sep_cedula(curp: str, paterno: str = None, materno: str = None, **kwargs):
    """Obtiene cédulas SEP por CURP. La firma antigua (nombres, paterno, materno) está deprecada."""
    if paterno is not None:
        warnings.warn(
            "obtain_sep_cedula(nombres, paterno, materno) está deprecado y ya no es funcional. "
            "El endpoint de SEP ahora requiere CURP. "
            "Use: obtain_sep_cedula(curp='XEXX010101MNEXXXA4')",
            DeprecationWarning, stacklevel=2
        )
        raise TypeError(
            "La firma obtain_sep_cedula(nombres, paterno, materno) ya no está soportada. "
            "El endpoint cambió y ahora requiere CURP. "
            "Use: obtain_sep_cedula('XEXX010101MNEXXXA4')"
        )
    return _obtain_sep_cedula(curp, **kwargs)


@format_api
@inject()
def validate_sat_data(nombre: str, rfc: str, regimen: str, cp: str, client: ApiMarketClient = None,
                      configuration: RequestConfiguration = None) -> Union[
    Future[ValidarDatosPostResponse], ValidarDatosPostResponse]:
    rules.text("nombre", nombre)
    validate_rfc(rfc)
    rules.text("regimen", regimen, min_length=3)
    rules.text("cp", cp, min_length=3)
    return client.api.sat.grupo.validar_datos.post, configuration


@format_api
@inject()
def search_credit_by_nss(nss: str, client: ApiMarketClient = None, configuration: RequestConfiguration = None) -> Union[
    Future[BuscarCreditoPostResponse], BuscarCreditoPostResponse]:
    validate_nss(nss)
    return client.api.infonavit.grupo.buscar_credito.post, configuration


@format_api
@inject()
def get_infonavit_subaccount(nss: str, client: ApiMarketClient = None, configuration: RequestConfiguration = None) -> \
        Union[Future[ObtenerCuentaPostResponse], ObtenerCuentaPostResponse]:
    validate_nss(nss)
    return client.api.infonavit.grupo.obtener_cuenta.post, configuration


@format_api
@inject()
def get_mexican_fiscal_data_with_rfc(rfc: str, client: ApiMarketClient = None,
                                     configuration: RequestConfiguration = None) -> Union[
    Future[ObtenerDatosPostResponse], ObtenerDatosPostResponse]:
    validate_rfc(rfc)
    return client.api.sat.grupo.obtener_datos.post, configuration


@format_api
@inject()
def search_sat_lista69b(rfc: str = None, nombre_contribuyente: str = None,
                        client: ApiMarketClient = None,
                        configuration: RequestConfiguration = None) -> Union[
    Future[Lista69bPostResponse], Lista69bPostResponse]:
    if not rfc and not nombre_contribuyente:
        raise InvalidParameterError.of("rfc, nombre_contribuyente", "MISSING",
                                       "Indique 'rfc' o 'nombre_contribuyente'.")
    if rfc is not None:
        validate_rfc(rfc)
    rules.optional_text("nombre_contribuyente", nombre_contribuyente)
    return client.api.sat.v2.lista69b.post, configuration


@format_api
@inject()
def retrieve_permissions(client: ApiMarketClient = None, configuration: RequestConfiguration = None):
    return client.api.v2.apimarket.permissions.get, configuration


# ---------------------------------------------------------------------------
# Backward-compatibility aliases — estas funciones fueron renombradas en v4.6.
# Emiten DeprecationWarning al ser llamadas; serán eliminadas en una versión futura.
# ---------------------------------------------------------------------------

def get_clinica_by_curp(curp: str, **kwargs):
    """Deprecado. Use get_clinic_by_curp()."""
    warnings.warn(
        "get_clinica_by_curp() está deprecado. Use get_clinic_by_curp() en su lugar.",
        DeprecationWarning, stacklevel=2
    )
    return get_clinic_by_curp(curp, **kwargs)


def consult_clinica_by_curp(curp: str, **kwargs):
    """Deprecado. Use consult_clinic_by_curp()."""
    warnings.warn(
        "consult_clinica_by_curp() está deprecado. Use consult_clinic_by_curp() en su lugar.",
        DeprecationWarning, stacklevel=2
    )
    return consult_clinic_by_curp(curp, **kwargs)


@inject()
def idse_list_certificates(client: ApiMarketClient = None, configuration: RequestConfiguration = None):
    if not di["IDSEPRO_BEARER_TOKEN"] or not di["IDSEPRO_API_KEY"]:
        raise ConfigurationError(ConfigurationError.Code.IDSE_CREDENTIALS_MISSING,
                                 "Configure IDSEPRO_BEARER_TOKEN e IDSEPRO_API_KEY.")
    idse_headers = HeadersCollection()
    idse_headers.try_add("Authorization", f"Bearer {di['IDSEPRO_BEARER_TOKEN']}")
    idse_headers.try_add("apikey", di["IDSEPRO_API_KEY"])
    idse_config = RequestConfiguration(headers=idse_headers)
    return choice_process_scheduler(
        lambda: client.api.imss.grupo.idse_pro.certificados.listar_certificados.get(idse_config)
    )()


# Servicios declarativos (se importan al final porque usan choice_process_scheduler).
from apimarket.services import *  # noqa: E402,F401,F403
