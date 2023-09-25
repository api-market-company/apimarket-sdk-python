import sys
import requests
from decouple import config

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
    url = f"https://apimarket.mx/api/imss/grupo/localizar-nss?curp={curp}"
    
    headers = create_basic_headers(api_key)
    
    response = requests.post(url, headers=headers)
    return response.json()['data']


def check_vigency(nss, curp, api_key=False):
    url = f"https://apimarket.mx/api/imss/grupo/consultar-vigencia?nss={nss}&curp={curp}"
    
    headers = create_basic_headers(api_key)
    
    response = requests.post(url, headers=headers)
    return response.json()['data']


def get_clinica_by_curp(curp, api_key=False):
    url = f"https://apimarket.mx/api/imss/grupo/con-clinica?curp={curp}"
    
    headers = create_basic_headers(api_key)
    
    response = requests.post(url, headers=headers)
    return response.json()['data']


def consult_clinica_by_curp(curp, api_key=False):
    url = f"https://apimarket.mx/api/imss/grupo/con-clinica?curp={curp}"
    
    headers = create_basic_headers(api_key)
    
    response = requests.post(url, headers=headers)
    return response.json()['data']

def get_labor_history(curp, nss, api_key=False):
    url = f"https://apimarket.mx/api/imss/grupo/historial-laboral?curp={curp}&nss={nss}"
    
    headers = create_basic_headers(api_key)
    
    response = requests.post(url, headers=headers)
    return response.json()['data']


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
    url = f"https://apimarket.mx/api/sat/grupo/validar-datos?nombre={nombre}&rfc={rfc}&regimen={regimen}&cp={cp}"
    
    headers = create_basic_headers(api_key)
    
    response = requests.post(url, headers=headers)
    return response.json()['data']

def search_credit_by_nss(nss, api_key=False):
    url = f"https://apimarket.mx/api/infonavit/grupo/buscar-credito?nss={nss}"
    
    headers = create_basic_headers(api_key)
    
    response = requests.post(url, headers=headers)
    return response.json()['data']
