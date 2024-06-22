import asyncio
import inspect
import sys
from asyncio import Future
from dataclasses import make_dataclass
from typing import Union

import nest_asyncio
from decouple import config
from kink import inject, di
from kiota_abstractions.authentication import AccessTokenProvider, AllowedHostsValidator, \
    BaseBearerTokenAuthenticationProvider
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_abstractions.headers_collection import HeadersCollection
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from kiota_serialization_json.json_serialization_writer import JsonSerializationWriter

from apimarket.api.imss.grupo.historial_laboral.historial_laboral_post_response import HistorialLaboralPostResponse
from apimarket.api.infonavit.grupo.buscar_credito.buscar_credito_post_response import BuscarCreditoPostResponse
from apimarket.api.infonavit.grupo.obtener_cuenta.obtener_cuenta_post_response import ObtenerCuentaPostResponse
from apimarket.api.renapo.grupo.obtener_curp.obtener_curp_post_response import ObtenerCurpPostResponse
from apimarket.api.sat.grupo.calcular_rfc.calcular_rfc_post_response import CalcularRfcPostResponse
from apimarket.api.sat.grupo.obtener_datos.obtener_datos_post_response import ObtenerDatosPostResponse
from apimarket.api.sat.grupo.obtener_rfc.obtener_rfc_post_response import ObtenerRfcPostResponse
from apimarket.api.sat.grupo.validar_datos.validar_datos_post_response import ValidarDatosPostResponse
from apimarket.api.sep.grupo.obtener_cedula.obtener_cedula_post_response import ObtenerCedulaPostResponse
from apimarket.api.sep.grupo.validar_cedula.validar_cedula_post_response import ValidarCedulaPostResponse
from apimarket.api.sep.grupo.validar_certificado.validar_certificado_post_response import ValidarCertificadoPostResponse
from apimarket.api_market_client import ApiMarketClient
from apimarket.models.curp_a_p_i_response import CurpAPIResponse
from apimarket.models.historial_data import HistorialData
from apimarket.validations import validate_curp, validate_rfc, validate_nss

nest_asyncio.apply()


class EnvironmentTokenProvider(AccessTokenProvider):
    def __init__(self, token=""):
        self.token = token

    async def get_authorization_token(self, uri: str, additional_authentication_context=None) -> str:
        if additional_authentication_context is None:
            additional_authentication_context = {}
        return self.token

    def get_allowed_hosts_validator(self) -> AllowedHostsValidator:
        pass


def assemble(api_key: str = "", headers: dict[str, str] = None, sandbox: bool = False, async_client: bool = False):
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
    di[EnvironmentTokenProvider] = lambda di: EnvironmentTokenProvider(di["API_MARKET_API_KEY"])
    di[AccessTokenProvider] = lambda di: BaseBearerTokenAuthenticationProvider(di[EnvironmentTokenProvider])
    di[RequestAdapter] = lambda di: HttpxRequestAdapter(di[AccessTokenProvider])
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


def get_an_event_loop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        return asyncio.new_event_loop()


def choice_process_scheduler(func):
    def wrapper(*args, **kwargs):
        if di["async_client"]:
            return func(*args, **kwargs)
        loop = get_an_event_loop()
        return loop.run_until_complete(func(*args, **kwargs))

    return wrapper


def format_api(func):
    def wrapper(*args, **kwargs):
        # Get the function's argument names and default values
        func_signature = inspect.signature(func)
        bound_arguments = func_signature.bind(*args, **kwargs)
        bound_arguments.apply_defaults()

        # Extract the arguments as a dictionary
        arguments = bound_arguments.arguments

        api, configuration = func(*args, **kwargs)

        configuration.query_parameters = make_query_params(arguments)

        return choice_process_scheduler(lambda: api(request_configuration=configuration))()

    return wrapper


def to_json(response):
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
def get_curp_from_details(nombres: str, paterno: str, materno: str, diaNacimiento: int, mesNacimiento: int,
                          anoNacimiento: int, claveEntidad: str, sexo: str, client: ApiMarketClient = None,
                          configuration: RequestConfiguration = None) -> Union[
    Future[ObtenerCurpPostResponse], ObtenerCurpPostResponse]:
    return client.api.renapo.grupo.obtener_curp.post, configuration


@format_api
@inject()
def get_rfc_from_curp(curp: str, client: ApiMarketClient = None, configuration: RequestConfiguration = None) -> Union[
    Future[ObtenerRfcPostResponse], ObtenerRfcPostResponse]:
    validate_curp(curp)
    return client.api.sat.grupo.obtener_rfc.post, configuration


@format_api
@inject()
def calculate_rfc(nombres: str, paterno: str, materno: str, diaNacimiento: int, mesNacimiento: int, anoNacimiento: int,
                  client: ApiMarketClient = None, configuration: RequestConfiguration = None) -> Union[
    Future[CalcularRfcPostResponse], CalcularRfcPostResponse]:
    return client.api.sat.grupo.calcular_rfc.post, configuration


@format_api
@inject()
def locate_umf_by_cp(cp: str, client: ApiMarketClient = None, configuration: RequestConfiguration = None):
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
def get_clinica_by_curp(curp: str, client: ApiMarketClient = None, configuration: RequestConfiguration = None):
    validate_curp(curp)
    return client.api.imss.grupo.con_clinica.post, configuration


@format_api
@inject()
def consult_clinica_by_curp(curp: str, client: ApiMarketClient = None, configuration: RequestConfiguration = None):
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
    return client.api.sep.grupo.validar_cedula.post, configuration


@format_api
@inject()
def validate_sep_certificate(folio: str, client: ApiMarketClient = None, configuration: RequestConfiguration = None) -> \
        Union[Future[ValidarCertificadoPostResponse], ValidarCertificadoPostResponse]:
    return client.api.sep.grupo.validar_certificado.post, configuration


@format_api
@inject()
def obtain_sep_cedula(nombres: str, paterno: str, materno: str, client: ApiMarketClient = None,
                      configuration: RequestConfiguration = None) -> Union[
    Future[ObtenerCedulaPostResponse], ObtenerCedulaPostResponse]:
    return client.api.sep.grupo.obtener_cedula.post, configuration


@format_api
@inject()
def validate_sat_data(nombre: str, rfc: str, regimen: str, cp: str, client: ApiMarketClient = None,
                      configuration: RequestConfiguration = None) -> Union[
    Future[ValidarDatosPostResponse], ValidarDatosPostResponse]:
    validate_rfc(rfc)
    return client.api.sat.grupo.validar_datos.post, configuration


@format_api
@inject()
def search_credit_by_nss(nss: str, client: ApiMarketClient = None, configuration: RequestConfiguration = None) -> Union[
    Future[BuscarCreditoPostResponse], BuscarCreditoPostResponse]:
    validate_nss(nss)
    return client.api.infonavit.grupo.buscar_credito.post, configuration


@format_api
@inject()
def verify_sat_signature(rfc: str, password: str, certificate: str, privateKey: str, client: ApiMarketClient = None,
                         configuration: RequestConfiguration = None):
    validate_rfc(rfc)
    return client.api.sat.grupo.verificar_firma_electronica.post, configuration


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
def store_token(name: str, company: str = "", description: str = "", permissions: list = None, rfc: str = "",
                ciec: str = "", client: ApiMarketClient = None, configuration: RequestConfiguration = None):
    if permissions is None:
        permissions = []
    if rfc:
        validate_rfc(rfc)
    return client.api.v2.apimarket.tokens.post, configuration


@format_api
@inject()
def retrieve_permissions(client: ApiMarketClient = None, configuration: RequestConfiguration = None):
    return client.api.v2.apimarket.permissions.get, configuration
