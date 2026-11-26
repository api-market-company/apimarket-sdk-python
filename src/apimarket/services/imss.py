"""Servicios del IMSS, incluido IDSE."""
from typing import Any, Dict, List, Optional

from apimarket import rules
from apimarket.services import _idse
from apimarket.services._core import Call, reset_header, service
from apimarket.validations import validate_curp, validate_nss


@service("imss", "pension", "/api/imss/grupo/consultar-pension")
def get_imss_pension(nss: str):
    """Consulta la pensión del IMSS por NSS."""
    validate_nss(nss)
    return Call(query={"nss": nss})


@service("imss", "historial-laboral-lite", "/api/imss/grupo/historial-laboral-lite")
def get_labor_history_lite(curp: str, email: str, nss: Optional[str] = None):
    """Solicita el historial laboral en versión ligera."""
    validate_curp(curp)
    rules.email("email", email)
    if nss is not None:
        validate_nss(nss)
    return Call(query={"curp": curp, "email": email, "nss": nss})


@service("imss", "rpci", "/api/imss/grupo/rpci")
def get_rpci(curp: str, correo: Optional[str] = None, nss: Optional[str] = None, reset: bool = False):
    """Consulta el servicio RPCI del IMSS."""
    validate_curp(curp)
    if correo is not None:
        rules.email("correo", correo)
    if nss is not None:
        validate_nss(nss)
    return Call(query={"curp": curp, "correo": correo, "nss": nss}, headers=reset_header(reset))


@service("imss", "trayectoria-laboral", "/api/imss/grupo/trayectoria-laboral")
def get_employment_trajectory(identificador: str):
    """Genera el reporte de trayectoria laboral.

    :param identificador: dato que identifica a la persona, por ejemplo su CURP.
    """
    rules.identifier("identificador", identificador)
    return Call(query={"identificador": identificador})


@service("imss", "umf-asignada", "/api/imss/grupo/umf-asignada")
def get_assigned_umf(nss: str):
    """Consulta la UMF asignada a un NSS."""
    validate_nss(nss)
    return Call(query={"nss": nss})


@service("imss", "datos-nss", "/api/imss/grupo/obtener-datos-nss")
def get_nss_data(nss: str):
    """Obtiene los datos asociados a un NSS."""
    validate_nss(nss)
    return Call(query={"nss": nss})


@service("imss", "idse-capturar", "/api/imss/grupo/idse/capturar-movimientos-afiliatorios", retry=False)
def idse_capture_movements(movimientos: List[Dict[str, Any]], webhook: str,
                           credentials: Optional[Dict[str, str]] = None, delay: Optional[str] = None):
    """Envía movimientos afiliatorios a IDSE.

    :param movimientos: lista de movimientos con los campos de la documentación.
    :param webhook: URL pública que recibe el resultado.
    :param credentials: ``userId``, ``password``, ``certificate`` y ``privateKey``.
    :param delay: fecha en la que debe procesarse el lote.
    """
    _idse.movements(movimientos)
    rules.https_url("webhook", webhook)
    if credentials is not None:
        _idse.credentials(credentials)
    if delay is not None:
        rules.date("delay", delay)
    return Call(json={"movimientos": movimientos, "webhook": webhook,
                      "credentials": credentials, "delay": delay})


@service("imss", "idse-consultar", "/api/imss/grupo/idse/consultar-movimientos-afiliatorios", retry=False)
def idse_get_movements_status(lote: int, webhook: str, credentials: Dict[str, str],
                              codigo_validacion_relacionado: str, page_size: Optional[int] = None):
    """Consulta el resultado de un lote de movimientos afiliatorios.

    :param lote: número de lote devuelto al capturar los movimientos.
    :param credentials: ``userId``, ``password``, ``certificate`` y ``privateKey``.
    :param codigo_validacion_relacionado: código de validación de la captura.
    """
    rules.integer("lote", lote, minimum=0)
    rules.https_url("webhook", webhook)
    _idse.credentials(credentials)
    rules.text("codigo_validacion_relacionado", codigo_validacion_relacionado, min_length=20, max_length=20)
    if page_size is not None:
        rules.integer("page_size", page_size, minimum=1, maximum=10000)
    return Call(json={"lote": lote, "webhook": webhook, "credentials": credentials,
                      "codigoDeValidacionRelacionado": codigo_validacion_relacionado,
                      "pageSize": page_size})


@service("imss", "idse-registros-patronales", "/api/imss/grupo/idse/registros-patronales", retry=False)
def idse_get_employer_registrations(webhook: str, credentials: Optional[Dict[str, str]] = None):
    """Solicita los registros patronales disponibles en IDSE."""
    rules.https_url("webhook", webhook)
    if credentials is not None:
        _idse.credentials(credentials)
    return Call(json={"webhook": webhook, "credentials": credentials})
