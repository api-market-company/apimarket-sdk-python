"""Servicios de la cuenta y de geolocalización."""
import warnings
from typing import List, Optional

from apimarket import rules
from apimarket.services._core import Call, service
from apimarket.validations import validate_rfc


@service("cuenta", "saldo", "/api/balance", method="GET")
def get_balance():
    """Consulta el saldo disponible de la cuenta."""
    return Call()


@service("cuenta", "llave-publica", "/api/v2/apimarket/public-key", method="GET")
def get_public_key():
    """Obtiene la llave pública de API Market."""
    return Call()


@service("cuenta", "crear-token", "/api/v2/apimarket/tokens", retry=False)
def store_token(name: str, company: str = "", description: str = "", permissions: Optional[List[str]] = None,
                rfc: str = "", ciec: str = ""):
    """Crea un token en la cuenta.

    :param permissions: permisos del token; vea ``retrieve_permissions()``.
    :param rfc: obsoleto, la API no lo recibe en este servicio.
    :param ciec: obsoleto, la API no lo recibe en este servicio.
    """
    rules.text("name", name)
    for permission in rules.items("permissions", permissions):
        rules.text("permissions", permission)
    for key, value in (("company", company), ("description", description), ("ciec", ciec)):
        if value != "":
            rules.optional_text(key, value)
    if rfc:
        validate_rfc(rfc)
    if rfc or ciec:
        warnings.warn("store_token() ya no envía 'rfc' ni 'ciec': la API no los recibe al crear tokens.",
                      DeprecationWarning, stacklevel=3)
    return Call(json={
        "name": name,
        "empresa": company or None,
        "description": description or None,
        "permissions": list(permissions),
    })


@service("geo", "codigos-postales", "/api/v2/codigos-postales")
def search_postal_codes(postal_code_mx: Optional[str] = None, postal_code: Optional[str] = None,
                        country_code: Optional[str] = None, select: Optional[str] = None):
    """Busca códigos postales.

    :param postal_code: filtro con operador, por ejemplo ``eq.10001``.
    :param country_code: filtro con operador, por ejemplo ``eq.US``.
    :param select: columnas separadas por comas.
    """
    if postal_code_mx is not None:
        rules.digits("postal_code_mx", postal_code_mx, 5, 5)
    for key, value in (("postal_code", postal_code), ("country_code", country_code)):
        if value is not None:
            rules.operator_filter(key, value)
    rules.optional_text("select", select)
    return Call(query={"postal_code_mx": postal_code_mx, "postal_code": postal_code,
                       "country_code": country_code, "select": select})
