import sys
import requests
from decouple import config
import re

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
    if len(nss) >= 11:
        return int(nss[10])
    
    acc = 0
    for i in range(10):
        if i & 1: 
            x = int(nss[i]) * 2
            acc += x % 10 + (1 if x >= 10 else 0)
        else:
            acc += int(nss[i])
    
    return str((10 - acc % 10)%10)

def calculate_curp_verification_digit(curp17):
    """Calculate the check digit for a CURP."""
    diccionario  = "0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
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

    if curp[17] !=  calculate_curp_verification_digit(curp[:17]):
        raise InvalidCURPError(curp, "CURP has an invalid check digit.")

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


def create_basic_headers(api_key=False):
    api_key = config('APIMARKET_API_KEY',default=api_key)
    if api_key == "" or api_key == False:
        raise InvalidAuthenticationToken()
    return {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }

def fetch_curp_details(curp,api_key=False):
    validate_curp(curp)
    url = f"https://apimarket.mx/api/renapo/grupo/valida-curp?curp={curp}"
    
    headers = create_basic_headers(api_key)

    response = requests.post(url, headers=headers)
    return response.json()['data']


def get_curp_from_details(nombres, paterno, materno, diaNacimiento, mesNacimiento, anoNacimiento, claveEntidad, sexo, api_key=False):
    url = f"https://apimarket.mx/api/renapo/grupo/obtener-curp?nombres={nombres}&paterno={paterno}&materno={materno}&diaNacimiento={diaNacimiento}&mesNacimiento={mesNacimiento}&anoNacimiento={anoNacimiento}&claveEntidad={claveEntidad}&sexo={sexo}"
    
    headers = create_basic_headers(api_key)
    
    response = requests.post(url, headers=headers)
    return response.json()['data']


def get_rfc_from_curp(curp, api_key=False):
    validate_curp(curp)
    url = f"https://apimarket.mx/api/sat/grupo/obtener-rfc?curp={curp}"
    
    headers = create_basic_headers(api_key)
    
    response = requests.post(url, headers=headers)
    return response.json()['data']

def calculate_rfc(nombres, paterno, materno, diaNacimiento, mesNacimiento, anoNacimiento, api_key=False):
    url = f"https://apimarket.mx/api/sat/grupo/calcular-rfc?nombres={nombres}&paterno={paterno}&materno={materno}&diaNacimiento={diaNacimiento}&mesNacimiento={mesNacimiento}&anoNacimiento={anoNacimiento}"
    
    headers = create_basic_headers(api_key)
    
    response = requests.post(url, headers=headers)
    return response.json()['data']


def locate_umf_by_cp(cp, api_key=False):
    url = f"https://apimarket.mx/api/imss/grupo/localizar-umf?cp={cp}"
    
    headers = create_basic_headers(api_key)
    
    response = requests.post(url, headers=headers)
    return response.json()['data']


def locate_nss_by_curp(curp, api_key=False):
    validate_curp(curp)
    url = f"https://apimarket.mx/api/imss/grupo/localizar-nss?curp={curp}"
    
    headers = create_basic_headers(api_key)
    
    response = requests.post(url, headers=headers)
    return response.json()['data']


def check_vigency(nss, curp, api_key=False):
    validate_curp(curp)
    validate_nss(nss)
    url = f"https://apimarket.mx/api/imss/grupo/consultar-vigencia?nss={nss}&curp={curp}"
    
    headers = create_basic_headers(api_key)
    
    response = requests.post(url, headers=headers)
    return response.json()['data']


def get_clinica_by_curp(curp, api_key=False):
    validate_curp(curp)
    url = f"https://apimarket.mx/api/imss/grupo/con-clinica?curp={curp}"
    
    headers = create_basic_headers(api_key)
    
    response = requests.post(url, headers=headers)
    return response.json()['data']


def consult_clinica_by_curp(curp, api_key=False):
    validate_curp(curp)
    url = f"https://apimarket.mx/api/imss/grupo/con-clinica?curp={curp}"
    
    headers = create_basic_headers(api_key)
    
    response = requests.post(url, headers=headers)
    return response.json()['data']

def get_labor_history(curp, nss, api_key=False):
    validate_curp(curp)
    validate_nss(nss)
    url = f"https://apimarket.mx/api/imss/grupo/historial-laboral?curp={curp}&nss={nss}"
    
    headers = create_basic_headers(api_key)
    
    response = requests.post(url, headers=headers)
    
    return response.json()


def validate_cedula(cedula, api_key=False):
    url = f"https://apimarket.mx/api/sep/grupo/validar-cedula?cedula={cedula}"
    
    headers = create_basic_headers(api_key)
    
    response = requests.post(url, headers=headers)
    return response.json()['data']


def validate_certificate(folio, api_key=False):
    url = f"https://apimarket.mx/api/sep/grupo/validar-certificado?folio={folio}"
    
    headers = create_basic_headers(api_key)
    
    response = requests.post(url, headers=headers)
    return response.json()['data']


def obtain_cedula(nombres, paterno, materno, api_key=False):
    url = f"https://apimarket.mx/api/sep/grupo/obtener-cedula?nombres={nombres}&paterno={paterno}&materno={materno}"
    
    headers = create_basic_headers(api_key)
    
    response = requests.post(url, headers=headers)
    return response.json()['data']

def validate_sat_data(nombre, rfc, regimen, cp, api_key=False):
    validate_rfc(rfc)
    url = f"https://apimarket.mx/api/sat/grupo/validar-datos?nombre={nombre}&rfc={rfc}&regimen={regimen}&cp={cp}"
    
    headers = create_basic_headers(api_key)
    
    response = requests.post(url, headers=headers)
    return response.json()['data']

def search_credit_by_nss(nss, api_key=False):
    validate_nss(nss)
    url = f"https://apimarket.mx/api/infonavit/grupo/buscar-credito?nss={nss}"
    
    headers = create_basic_headers(api_key)
    
    response = requests.post(url, headers=headers)
    return response.json()['data']
