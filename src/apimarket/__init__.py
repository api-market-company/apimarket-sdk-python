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


def fetch_curp_details(curp,api_key=False):
    url = f"https://apimarket.mx/api/renapo/grupo/valida-curp?curp={curp}"
    headers = {
        "Authorization": f"Bearer {config('APIMARKET_API_KEY',default=api_key)}",
        "Accept": "application/json",
    }
    response = requests.post(url, headers=headers)
    return response.json()['data']