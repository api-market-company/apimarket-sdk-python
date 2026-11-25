"""Servicios de INFONAVIT.

Estas rutas viven bajo ``/api/v2/infonavit``. El OpenAPI publicado las lista sin
el prefijo ``v2`` y esas direcciones responden 404.
"""
from apimarket import rules
from apimarket.services._core import Call, service
from apimarket.validations import validate_credit_number, validate_nss

_BASE = "/api/v2/infonavit"


@service("infonavit", "ficha-tecnica", f"{_BASE}/ficha-tecnica")
def get_infonavit_technical_sheet(identificador: str):
    """Genera la ficha técnica del crédito.

    :param identificador: NSS, RFC, número de crédito o CURP.
    """
    rules.identifier("identificador", identificador, allow_credit=True)
    return Call(query={"identificador": identificador})


@service("infonavit", "datos-acreditado", f"{_BASE}/datos-acreditado")
def get_infonavit_borrower_data(identificador: str):
    """Obtiene los datos del acreditado.

    :param identificador: NSS, RFC, número de crédito o CURP.
    """
    rules.identifier("identificador", identificador, allow_credit=True)
    return Call(query={"identificador": identificador})


@service("infonavit", "datos-contacto", f"{_BASE}/obtener-datos-contacto")
def get_infonavit_contact_data(nss: str):
    """Obtiene los datos de contacto por NSS."""
    validate_nss(nss)
    return Call(query={"nss": nss})


def _credit(num_credito: str) -> Call:
    rules.required(num_credito=num_credito)
    validate_credit_number(num_credito)
    return Call(query={"num_credito": num_credito})


@service("infonavit", "historico", f"{_BASE}/historico")
def get_infonavit_credit_history(num_credito: str):
    """Consulta el histórico de un crédito."""
    return _credit(num_credito)


@service("infonavit", "datos-financieros", f"{_BASE}/datos-financieros")
def get_infonavit_financial_data(num_credito: str):
    """Consulta los datos financieros de un crédito."""
    return _credit(num_credito)


@service("infonavit", "datos-cobranza", f"{_BASE}/datos-cobranza")
def get_infonavit_collection_data(num_credito: str):
    """Consulta los datos de cobranza de un crédito."""
    return _credit(num_credito)


@service("infonavit", "reporte-historico", f"{_BASE}/obtener-historico-credito")
def get_infonavit_credit_history_report(num_credito: str):
    """Obtiene el reporte histórico de un crédito."""
    return _credit(num_credito)


@service("infonavit", "estado-cuenta", f"{_BASE}/obtener-estado-cuenta")
def get_infonavit_account_statement(num_credito: str):
    """Obtiene el estado de cuenta de un crédito."""
    return _credit(num_credito)


@service("infonavit", "reporte-intereses", f"{_BASE}/obtener-reporte-intereses")
def get_infonavit_interest_report(num_credito: str):
    """Obtiene el reporte de intereses de un crédito."""
    return _credit(num_credito)
