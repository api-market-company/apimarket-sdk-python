import re
import sys

from decouple import config
import ssl
import httpx
from tenacity import retry, retry_if_exception_type
import hishel

controller = hishel.Controller(
    cacheable_methods=["GET", "POST"],
    cacheable_status_codes=[200],
    allow_stale=True,
    always_revalidate=True
)

ssl_context = ssl.create_default_context()
ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3
ssl_context.maximum_version = ssl.TLSVersion.TLSv1_3

transport = httpx.HTTPTransport(retries=3)
storage = hishel.FileStorage()

requests = hishel.CacheClient(controller=controller,
                              http2=True,
                              verify=ssl_context,
                              transport=transport,
                              storage=storage
                              )

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


class ServiceError(Exception):
    def __init__(self, service, params, message):
        self.params = params
        self.message = message
        self.service = service
        super().__init__(self.message)

    def __str__(self):
        return f"ServiceError({self.service}): {self.params} - {self.message}"


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


class InvalidAuthenticationToken(Exception):
    def __init__(self):
        self.message = "Please check whether the token has been set. You must either call the function with your token or set an environment variable."
        super().__init__(self.message)


def create_headers(api_key=False):
    api_key = config('APIMARKET_API_KEY', default=api_key)
    sandbox = config('APIMARKET_SANDBOX', default=False)
    if api_key == "" or not api_key:
        raise InvalidAuthenticationToken()
    headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json", "Content-Type": "application/json"}
    if sandbox:
        headers['x-sandbox'] = sandbox
    return headers


@retry(retry=retry_if_exception_type(httpx.TimeoutException) | retry_if_exception_type(
    httpx.ReadTimeout) | retry_if_exception_type(httpx.WriteTimeout))
def fetch_curp_details(curp, api_key=False):
    validate_curp(curp)
    url = f"https://apimarket.mx/api/renapo/grupo/valida-curp?curp={curp}"

    headers = create_headers(api_key)

    response = requests.post(url, headers=headers)

    body = response.json()
    if response.status_code != 200 or 'data' not in body:
        raise ServiceError("fetch_curp_details", curp, body)

    return body['data']


@retry(retry=retry_if_exception_type(httpx.TimeoutException) | retry_if_exception_type(
    httpx.ReadTimeout) | retry_if_exception_type(httpx.WriteTimeout))
def get_curp_from_details(nombres, paterno, materno, diaNacimiento, mesNacimiento, anoNacimiento, claveEntidad, sexo,
                          api_key=False):
    url = f"https://apimarket.mx/api/renapo/grupo/obtener-curp?nombres={nombres}&paterno={paterno}&materno={materno}&diaNacimiento={diaNacimiento}&mesNacimiento={mesNacimiento}&anoNacimiento={anoNacimiento}&claveEntidad={claveEntidad}&sexo={sexo}"

    headers = create_headers(api_key)

    response = requests.post(url, headers=headers)
    body = response.json()
    if response.status_code != 200 or 'data' not in body:
        raise ServiceError("get_curp_from_details", f"{nombres} {paterno} {materno}", body)

    return body['data']['curp']


@retry(retry=retry_if_exception_type(httpx.TimeoutException) | retry_if_exception_type(
    httpx.ReadTimeout) | retry_if_exception_type(httpx.WriteTimeout))
def get_rfc_from_curp(curp, api_key=False):
    validate_curp(curp)
    url = f"https://apimarket.mx/api/sat/grupo/obtener-rfc?curp={curp}"

    headers = create_headers(api_key)

    response = requests.post(url, headers=headers)
    body = response.json()
    if response.status_code != 200 or 'data' not in body:
        raise ServiceError("get_rfc_from_curp", f"{curp}", body)
    return body['data']


@retry(retry=retry_if_exception_type(httpx.TimeoutException) | retry_if_exception_type(
    httpx.ReadTimeout) | retry_if_exception_type(httpx.WriteTimeout))
def calculate_rfc(nombres, paterno, materno, diaNacimiento, mesNacimiento, anoNacimiento, api_key=False):
    url = f"https://apimarket.mx/api/sat/grupo/calcular-rfc?nombres={nombres}&paterno={paterno}&materno={materno}&diaNacimiento={diaNacimiento}&mesNacimiento={mesNacimiento}&anoNacimiento={anoNacimiento}"

    headers = create_headers(api_key)

    response = requests.post(url, headers=headers)
    body = response.json()
    if response.status_code != 200 or 'data' not in body:
        raise ServiceError("calculate_rfc", f"{nombres} {paterno} {materno}", body)
    return body['data']


@retry(retry=retry_if_exception_type(httpx.TimeoutException) | retry_if_exception_type(
    httpx.ReadTimeout) | retry_if_exception_type(httpx.WriteTimeout))
def locate_umf_by_cp(cp, api_key=False):
    url = f"https://apimarket.mx/api/imss/grupo/localizar-umf?cp={cp}"

    headers = create_headers(api_key)

    response = requests.post(url, headers=headers)
    body = response.json()
    if response.status_code != 200 or 'data' not in body:
        raise ServiceError("locate_umf_by_cp", f"{cp}", body)
    return body['data']


@retry(retry=retry_if_exception_type(httpx.TimeoutException) | retry_if_exception_type(
    httpx.ReadTimeout) | retry_if_exception_type(httpx.WriteTimeout))
def locate_nss_by_curp(curp, api_key=False):
    validate_curp(curp)
    url = f"https://apimarket.mx/api/imss/grupo/localizar-nss?curp={curp}"

    headers = create_headers(api_key)

    response = requests.post(url, headers=headers)
    body = response.json()
    if response.status_code != 200 or 'data' not in body:
        raise ServiceError("locate_nss_by_curp", f"{curp}", body)
    return body['data']


@retry(retry=retry_if_exception_type(httpx.TimeoutException) | retry_if_exception_type(
    httpx.ReadTimeout) | retry_if_exception_type(httpx.WriteTimeout))
def check_nss_validity(nss, curp, api_key=False):
    validate_curp(curp)
    validate_nss(nss)
    url = f"https://apimarket.mx/api/imss/grupo/consultar-vigencia?nss={nss}&curp={curp}"

    headers = create_headers(api_key)

    response = requests.post(url, headers=headers)
    body = response.json()
    if response.status_code != 200 or 'data' not in body:
        raise ServiceError("locate_nss_by_curp", f"{curp}", body)
    return body['data']


@retry(retry=retry_if_exception_type(httpx.TimeoutException) | retry_if_exception_type(
    httpx.ReadTimeout) | retry_if_exception_type(httpx.WriteTimeout))
def get_clinica_by_curp(curp, api_key=False):
    validate_curp(curp)
    url = f"https://apimarket.mx/api/imss/grupo/con-clinica?curp={curp}"

    headers = create_headers(api_key)

    response = requests.post(url, headers=headers)
    body = response.json()
    if response.status_code != 200 or 'data' not in body:
        raise ServiceError("get_clinica_by_curp", f"{curp}", body)
    return body['data']


@retry(retry=retry_if_exception_type(httpx.TimeoutException) | retry_if_exception_type(
    httpx.ReadTimeout) | retry_if_exception_type(httpx.WriteTimeout))
def consult_clinica_by_curp(curp, api_key=False):
    validate_curp(curp)
    url = f"https://apimarket.mx/api/imss/grupo/con-clinica?curp={curp}"

    headers = create_headers(api_key)

    response = requests.post(url, headers=headers)
    body = response.json()
    if response.status_code != 200 or 'data' not in body:
        raise ServiceError("consult_clinica_by_curp", f"{curp}", body)
    return body['data']


@retry(retry=retry_if_exception_type(httpx.TimeoutException) | retry_if_exception_type(
    httpx.ReadTimeout) | retry_if_exception_type(httpx.WriteTimeout))
def get_labor_history(curp, nss, api_key=False):
    validate_curp(curp)
    validate_nss(nss)
    url = f"https://apimarket.mx/api/imss/grupo/historial-laboral?curp={curp}&nss={nss}"

    headers = create_headers(api_key)

    response = requests.post(url, headers=headers)
    body = response.json()
    if response.status_code != 200 or 'data' not in body:
        raise ServiceError("get_labor_history", f"{curp} {nss}", body)

    return body


@retry(retry=retry_if_exception_type(httpx.TimeoutException) | retry_if_exception_type(
    httpx.ReadTimeout) | retry_if_exception_type(httpx.WriteTimeout))
def validate_sep_cedula(cedula, api_key=False):
    url = f"https://apimarket.mx/api/sep/grupo/validar-cedula?cedula={cedula}"

    headers = create_headers(api_key)

    response = requests.post(url, headers=headers)
    body = response.json()
    if response.status_code != 200 or 'data' not in body:
        raise ServiceError("validate_cedula", f"Cedula: {cedula}", body)
    return body['data']


@retry(retry=retry_if_exception_type(httpx.TimeoutException) | retry_if_exception_type(
    httpx.ReadTimeout) | retry_if_exception_type(httpx.WriteTimeout))
def validate_sep_certificate(folio, api_key=False):
    url = f"https://apimarket.mx/api/sep/grupo/validar-certificado?folio={folio}"

    headers = create_headers(api_key)

    response = requests.post(url, headers=headers)
    body = response.json()
    if response.status_code != 200 or 'data' not in body:
        raise ServiceError("validate_certificate", f"Folio: {folio}", body)
    return body['data']


@retry(retry=retry_if_exception_type(httpx.TimeoutException) | retry_if_exception_type(
    httpx.ReadTimeout) | retry_if_exception_type(httpx.WriteTimeout))
def obtain_sep_cedula(nombres, paterno, materno, api_key=False):
    url = f"https://apimarket.mx/api/sep/grupo/obtener-cedula?nombres={nombres}&paterno={paterno}&materno={materno}"

    headers = create_headers(api_key)

    response = requests.post(url, headers=headers)
    body = response.json()
    if response.status_code != 200 or 'data' not in body:
        raise ServiceError("obtain_sep_cedula", f"{nombres} {paterno} {materno}", body)
    return body['data']


@retry(retry=retry_if_exception_type(httpx.TimeoutException) | retry_if_exception_type(
    httpx.ReadTimeout) | retry_if_exception_type(httpx.WriteTimeout))
def validate_sat_data(nombre, rfc, regimen, cp, api_key=False):
    validate_rfc(rfc)
    url = f"https://apimarket.mx/api/sat/grupo/validar-datos?nombre={nombre}&rfc={rfc}&regimen={regimen}&cp={cp}"

    headers = create_headers(api_key)

    response = requests.post(url, headers=headers)
    body = response.json()
    if response.status_code != 200 or 'data' not in body:
        raise ServiceError("validate_sat_data", f"{nombre} {rfc}", body)
    return body['data']


@retry(retry=retry_if_exception_type(httpx.TimeoutException) | retry_if_exception_type(
    httpx.ReadTimeout) | retry_if_exception_type(httpx.WriteTimeout))
def search_credit_by_nss(nss, api_key=False):
    validate_nss(nss)
    url = f"https://apimarket.mx/api/infonavit/grupo/buscar-credito?nss={nss}"

    headers = create_headers(api_key)

    response = requests.post(url, headers=headers)
    body = response.json()
    if response.status_code != 200 or 'data' not in body:
        raise ServiceError("search_credit_by_nss", f"{nss}", body)
    return body['data']


@retry(retry=retry_if_exception_type(httpx.TimeoutException) | retry_if_exception_type(
    httpx.ReadTimeout) | retry_if_exception_type(httpx.WriteTimeout))
def verify_sat_signature(rfc, password, certificate, privateKey,  api_key=False):
    validate_rfc(rfc)
    url = f"https://apimarket.mx/api/sat/grupo/verificar-firma-electronica"

    headers = create_headers(api_key)

    files = {
        'userId': rfc,
        'password': password,
        'certificate': open(certificate, 'rb'),
        'privateKey': open(privateKey, 'rb')
    }

    response = requests.post(url, headers=headers, files=files)

    body = response.json()
    if response.status_code != 200 or 'data' not in body:
        raise ServiceError("verify_sat_signature", f"{rfc}", body)
    return body['message']



@retry(retry=retry_if_exception_type(httpx.TimeoutException) | retry_if_exception_type(
    httpx.ReadTimeout) | retry_if_exception_type(httpx.WriteTimeout))
def get_infonavit_subaccount(nss, api_key=False):
    """
       Learn more on https://apimarket.mx/marketplace/obtener-subcuenta-de-vivienda
    """
    validate_nss(nss)
    url = f"https://apimarket.mx/api/infonavit/grupo/obtener-cuenta?nss={nss}"

    headers = create_headers(api_key)

    response = requests.post(url, headers=headers)
    body = response.json()
    if response.status_code != 200 or 'data' not in body:
        raise ServiceError("get_infonavit_subaccount", f"{nss}", body)
    return body['data']


@retry(retry=retry_if_exception_type(httpx.TimeoutException) | retry_if_exception_type(
    httpx.ReadTimeout) | retry_if_exception_type(httpx.WriteTimeout))
def get_mexican_fiscal_data_with_rfc(rfc, api_key=False):
    """
       Learn more on https://apimarket.mx/marketplace/obtener-datos-fiscales
    """
    validate_rfc(rfc)
    url = f"https://apimarket.mx/api/sat/grupo/obtener-datos?rfc={rfc}"

    headers = create_headers(api_key)

    response = requests.post(url, headers=headers)
    body = response.json()
    if response.status_code != 200 or 'data' not in body:
        raise ServiceError("mexican fiscal data", rfc, body)
    return body['data']


@retry(retry=retry_if_exception_type(httpx.TimeoutException) | retry_if_exception_type(
    httpx.ReadTimeout) | retry_if_exception_type(httpx.WriteTimeout))
def store_token(name, company="", description="", permissions=None, rfc="", ciec="", api_key=False):
    if permissions is None:
        permissions = []
    url = f"https://apimarket.mx/api/v2/apimarket/tokens"
    headers = create_headers(api_key)
    dynamic_body = {}
    if rfc != "":
        validate_rfc(rfc)
        dynamic_body['rfc'] = rfc
        dynamic_body['ciec'] = ciec
    response = requests.post(url, json={'name': name, 'description': description, 'permissions': permissions,
                                        'empresa': company, **dynamic_body}, headers=headers)
    body = response.json()
    if response.status_code != 200 or 'data' not in body:
        raise ServiceError("store_tokens", name, body)
    return body


@retry(retry=retry_if_exception_type(httpx.TimeoutException) | retry_if_exception_type(
    httpx.ReadTimeout) | retry_if_exception_type(httpx.WriteTimeout))
def retrieve_permissions(api_key=False):
    url = f"https://apimarket.mx/api/v2/apimarket/permissions"
    headers = create_headers(api_key)
    response = requests.get(url, headers=headers)
    body = response.json()
    if response.status_code != 200 or 'data' not in body:
        raise ServiceError("retrieve_permissions", "", body)
    return body
