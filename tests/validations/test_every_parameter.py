"""Cada parámetro de cada función pública rechaza datos inválidos antes de llamar a la API."""
import ast
import pathlib

import pytest

import apimarket
from apimarket.errors import CATALOG
from apimarket.validations import ValidationError

from arguments import LEGACY, NEW, VALID, signature

CATALOG_CODES = {code for _, _, codes in CATALOG for code, _ in codes}
BAD_FILE = "/no/existe"
LONG = "x" * 300

#: Un valor inválido para cada nombre de parámetro.
BAD = {
    "curp": "MALA", "rfc": "MAL", "nss": "123", "num_credito": "123", "cp": "123", "cedula": "abc",
    "folio": "no-uuid", "nombres": "", "paterno": "", "materno": 5, "diaNacimiento": "1", "mesNacimiento": "1",
    "anoNacimiento": "90", "claveEntidad": "99", "sexo": "Z", "nombre": "", "regimen": "1", "regimen_fiscal": "1",
    "nombre_contribuyente": 5, "name": "", "company": 5, "description": 5, "permissions": [5], "ciec": "corta",
    "postal_code_mx": "123", "postal_code": "10001", "country_code": "US", "select": 5, "reset": "si",
    "numero_serie": LONG, "placas": LONG, "email": "sin-arroba", "correo": "sin-arroba", "identificador": "abc",
    "movimientos": [{}], "webhook": "http://sin-https.example.com", "credentials": {"userId": "solo"},
    "delay": "mañana", "lote": "uno", "codigo_validacion_relacionado": "corto", "page_size": 0,
    "idcif": "abc", "csf": BAD_FILE, "codigo_postal": "1", "uso_cfdi": LONG, "password": "", "certificate": BAD_FILE,
    "privateKey": BAD_FILE, "year": 24, "periodicidad": "Z", "periodo": "13", "uuid": "", "fecha_inicial": "ayer",
    "fecha_final": "ayer", "rfc_receptor": "MAL", "rfc_tercero": "MAL", "rfc_emisor": "MAL",
    "estado_comprobante": 5, "tipo_comprobante": "Z", "complementos": "pago", "blob_path": "no-url",
    "formato": "doc", "anverso": BAD_FILE, "reverso": BAD_FILE, "template": BAD_FILE, "template_id": "",
    "inputs": [], "options": "texto", "wait": "no", "data": BAD_FILE, "resources": [{}], "dataset": "",
    "transaction_id": -1, "resource": "", "filter": {"a": {"mayor": 1}}, "sort": 5, "page": 0, "per_page": 101,
    "row_id": -1,
}
#: Casos en que el mismo nombre pide otro valor inválido.
SPECIAL = {
    ("validate_sat_data", "cp"): "1",
    ("search_sat_invoices", "uuid"): "no-uuid",
    ("download_sat_invoice", "uuid"): "no-uuid",
    ("store_token", "ciec"): 5,  # obsoleto: la API no lo recibe, solo se revisa el tipo
}


PARAMETERS = [(name, parameter) for name in VALID for parameter in signature(name)]


def public_functions():
    tree = ast.parse(pathlib.Path(apimarket.__file__).read_text())
    helpers = {"assemble", "make_query_params", "get_sync_event_loop", "ensure_api_key", "choice_process_scheduler",
               "format_api", "to_json"}
    return {node.name for node in tree.body
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_")} - helpers


def test_every_public_function_is_covered():
    assert public_functions() == set(LEGACY)
    assert set(VALID) == set(LEGACY) | set(NEW)


@pytest.mark.parametrize("name", sorted(VALID))
def test_valid_data_is_accepted(server, name):
    getattr(apimarket, name)(**VALID[name]) if name not in LEGACY else _call_legacy(name, VALID[name])
    assert len(server.requests) == 1


def _call_legacy(name, arguments):
    try:
        getattr(apimarket, name)(**arguments)
    except ValidationError:
        raise
    except Exception:
        pass  # el servidor local responde un formato genérico que los modelos tipados pueden no leer


@pytest.mark.parametrize("name, parameter", PARAMETERS, ids=[f"{n}-{p}" for n, p in PARAMETERS])
def test_invalid_parameter_has_a_code_and_never_reaches_api(server, name, parameter):
    arguments = {**VALID[name], parameter: SPECIAL.get((name, parameter), BAD[parameter])}
    with pytest.raises(ValidationError) as exc_info:
        getattr(apimarket, name)(**arguments)
    assert exc_info.value.code in CATALOG_CODES
    assert exc_info.value.message
    assert server.requests == []
