"""Argumentos válidos de cada función pública. Base de las pruebas de validación."""
import inspect

from apimarket.services import REGISTRY

from cases import CASES, CURP, NSS, RFC, UUID

NEW = {spec.function.__name__: spec.function for spec in REGISTRY}

#: Argumentos válidos de partida.
VALID = {name: dict(arguments) for name, arguments, _ in CASES}

PERSON = {"nombres": "JUAN", "paterno": "PEREZ", "materno": "LOPEZ", "diaNacimiento": "01",
          "mesNacimiento": "01", "anoNacimiento": "1990"}
LEGACY = {
    "fetch_curp_details": {"curp": CURP},
    "get_birth_record": {"curp": CURP},
    "get_curp_from_details": {**PERSON, "claveEntidad": "09", "sexo": "H"},
    "get_rfc_from_curp": {"curp": CURP},
    "calculate_rfc": PERSON,
    "locate_umf_by_cp": {"cp": "06600"},
    "locate_nss_by_curp": {"curp": CURP},
    "check_nss_validity": {"nss": NSS, "curp": CURP},
    "get_clinic_by_curp": {"curp": CURP},
    "consult_clinic_by_curp": {"curp": CURP},
    "get_clinica_by_curp": {"curp": CURP},
    "consult_clinica_by_curp": {"curp": CURP},
    "get_labor_history": {"curp": CURP, "nss": NSS},
    "validate_sep_cedula": {"cedula": "1234567"},
    "validate_sep_certificate": {"folio": UUID},
    "obtain_sep_cedula": {"curp": CURP},
    "validate_sat_data": {"nombre": "JUAN", "rfc": RFC, "regimen": "601", "cp": "06600"},
    "search_credit_by_nss": {"nss": NSS},
    "get_infonavit_subaccount": {"nss": NSS},
    "get_mexican_fiscal_data_with_rfc": {"rfc": RFC},
    "search_sat_lista69b": {"rfc": RFC, "nombre_contribuyente": "EMPRESA"},
    "retrieve_permissions": {},
    "idse_list_certificates": {},
}
VALID.update(LEGACY)
# Opcionales ausentes en la tabla de casos que dependen de otro parámetro.
VALID["get_sat_tax_returns"].update(periodicidad="M", periodo="3")
for receipt in ("get_sat_tax_return_receipt", "get_sat_tax_return_document"):
    VALID[receipt].update(uuid="u1", periodicidad="M", periodo="3")

def signature(name):
    """Parámetros reales de la función, sin los que inyecta el SDK."""
    if name in NEW:
        return list(inspect.signature(NEW[name]).parameters)
    return list(LEGACY[name])


PARAMETERS = [(name, parameter) for name in VALID for parameter in signature(name)]
