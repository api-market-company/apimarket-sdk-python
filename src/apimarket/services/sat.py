"""Servicios del SAT.

En los servicios ``/api/v2/sat`` el RFC y la CIEC son opcionales: si se omiten,
la API usa las credenciales guardadas en el token. Se envían en el cuerpo de la
petición para que no queden en la URL. También se aceptan cifrados con la llave
del token, por eso no se validan localmente.
"""
from typing import List, Optional

from apimarket import rules
from apimarket.services._core import Call, FileInput, reset_header, service
from apimarket.validations import InvalidParameterError, validate_rfc


# ---------------------------------------------------------------------------
# Grupo
# ---------------------------------------------------------------------------

@service("sat", "validar-rfc", "/api/sat/grupo/validar-rfc")
def check_sat_rfc(rfc: str):
    """Valida un RFC ante el SAT.

    No confundir con ``validate_rfc()``, que solo revisa el formato.
    """
    validate_rfc(rfc)
    return Call(query={"rfc": rfc})


@service("sat", "datos-idcif", "/api/sat/grupo/obtener-datos-idcif")
def get_fiscal_data_by_idcif(rfc: str, idcif: str):
    """Obtiene los datos fiscales con el RFC y el idCIF."""
    validate_rfc(rfc)
    rules.digits("idcif", idcif, 1, 20)
    return Call(query={"rfc": rfc, "idcif": idcif})


@service("sat", "leer-csf", "/api/sat/grupo/parse-csf")
def parse_csf(csf: FileInput):
    """Extrae los datos de una Constancia de Situación Fiscal (PDF o imagen)."""
    return Call(files={"csf": rules.load_file("csf", csf, extensions=rules.DOCUMENTS)})


@service("sat", "certificados-rfc", "/api/sat/grupo/obtener-certificados-rfc")
def get_rfc_certificates(rfc: str, reset: bool = False):
    """Obtiene los certificados asociados a un RFC."""
    validate_rfc(rfc)
    return Call(query={"rfc": rfc}, headers=reset_header(reset))


@service("sat", "validar-receptor", "/api/sat/grupo/validar-datos-receptor")
def validate_sat_receiver(rfc: str, nombre: str, codigo_postal: str, regimen_fiscal: str,
                          uso_cfdi: Optional[str] = None, correo: Optional[str] = None, reset: bool = False):
    """Valida los datos fiscales de un receptor de CFDI contra el padrón."""
    validate_rfc(rfc)
    rules.text("nombre", nombre, min_length=3, max_length=254)
    rules.digits("codigo_postal", codigo_postal, 5, 5)
    rules.digits("regimen_fiscal", regimen_fiscal, 3, 3)
    rules.optional_text("uso_cfdi", uso_cfdi, max_length=5)
    if correo is not None:
        rules.email("correo", correo)
    return Call(query={"rfc": rfc, "nombre": nombre, "codigo_postal": codigo_postal,
                       "regimen_fiscal": regimen_fiscal, "uso_cfdi": uso_cfdi, "correo": correo},
                headers=reset_header(reset))


@service("sat", "verificar-efirma", "/api/sat/grupo/verificar-firma-electronica")
def verify_sat_signature(rfc: str, password: str, certificate: FileInput, privateKey: FileInput):
    """Verifica una firma electrónica.

    :param certificate: archivo ``.cer``.
    :param privateKey: archivo ``.key``.
    """
    validate_rfc(rfc)
    rules.text("password", password)
    return Call(data={"userId": rfc, "password": password},
                files={"certificate": rules.load_file("certificate", certificate),
                       "privateKey": rules.load_file("privateKey", privateKey)})


_PERIODICITIES = ("M", "Y")
_YEARLY_PERIODS = ("0", "00", "000", "043")


def _period(periodicidad: Optional[str], periodo: Optional[str]) -> None:
    if periodicidad is None:
        if periodo is not None:
            raise InvalidParameterError.of("periodicidad", "COMBINATION",
                                           "Para filtrar por periodo indique también la periodicidad (M o Y).")
        return
    kind = rules.option("periodicidad", periodicidad, _PERIODICITIES, ignore_case=True)
    if kind == "M":
        month = int(rules.digits("periodo", periodo, 1, 3))
        rules.integer("periodo", month, minimum=1, maximum=12)
    elif periodo is not None:
        rules.option("periodo", periodo, _YEARLY_PERIODS)


# ---------------------------------------------------------------------------
# Portal del SAT con RFC y CIEC (v2)
# ---------------------------------------------------------------------------

def _portal(rfc: Optional[str], ciec: Optional[str], reset: bool = False, path_params: Optional[dict] = None,
            **body) -> Call:
    rules.sat_credentials(rfc, ciec)
    return Call(path_params=path_params or {}, json={"rfc": rfc, "ciec": ciec, **body},
                headers=reset_header(reset))


@service("sat", "informacion", "/api/v2/sat/informacion")
def get_sat_information(rfc: Optional[str] = None, ciec: Optional[str] = None):
    """Consulta la información general del contribuyente."""
    return _portal(rfc, ciec)


@service("sat", "csf", "/api/v2/sat/csf")
def get_sat_csf(rfc: Optional[str] = None, ciec: Optional[str] = None):
    """Obtiene la Constancia de Situación Fiscal."""
    return _portal(rfc, ciec)


@service("sat", "cif", "/api/v2/sat/cif")
def get_sat_cif(rfc: Optional[str] = None, ciec: Optional[str] = None):
    """Obtiene la Cédula de Identificación Fiscal."""
    return _portal(rfc, ciec)


@service("sat", "buzon-leidos", "/api/v2/sat/buzon/leidos")
def get_sat_read_messages(rfc: Optional[str] = None, ciec: Optional[str] = None):
    """Lista los mensajes leídos del buzón tributario."""
    return _portal(rfc, ciec)


@service("sat", "buzon-nuevos", "/api/v2/sat/buzon/nuevos")
def get_sat_unread_messages(rfc: Optional[str] = None, ciec: Optional[str] = None):
    """Lista los mensajes nuevos del buzón tributario."""
    return _portal(rfc, ciec)


@service("sat", "buzon-leer", "/api/v2/sat/buzon/leer/{uuid}", retry=False)
def read_sat_message(uuid: str, rfc: Optional[str] = None, ciec: Optional[str] = None):
    """Abre un mensaje del buzón tributario."""
    rules.text("uuid", uuid)
    return _portal(rfc, ciec, path_params={"uuid": uuid})


@service("sat", "buzon-medios-contacto", "/api/v2/sat/buzon/medios-contacto")
def get_sat_contact_methods(rfc: Optional[str] = None, ciec: Optional[str] = None, reset: bool = False):
    """Consulta los medios de contacto del buzón tributario."""
    return _portal(rfc, ciec, reset)


@service("sat", "declaraciones", "/api/v2/sat/declaraciones/{year}")
def get_sat_tax_returns(year: int, rfc: Optional[str] = None, ciec: Optional[str] = None,
                        periodicidad: Optional[str] = None, periodo: Optional[str] = None, reset: bool = False):
    """Lista las declaraciones de un ejercicio.

    :param periodicidad: ``M`` (mensual) o ``Y`` (del ejercicio).
    :param periodo: periodo según la periodicidad; requiere indicarla.
    """
    rules.integer("year", year, minimum=1000, maximum=9999)
    _period(periodicidad, periodo)
    return _portal(rfc, ciec, reset, {"year": year}, periodicidad=periodicidad, periodo=periodo)


@service("sat", "declaracion-acuse", "/api/v2/sat/declaraciones/obtener-acuse/{uuid}")
def get_sat_tax_return_receipt(uuid: str, rfc: Optional[str] = None, ciec: Optional[str] = None,
                               periodicidad: Optional[str] = None, periodo: Optional[str] = None):
    """Descarga el acuse de una declaración."""
    rules.text("uuid", uuid)
    _period(periodicidad, periodo)
    return _portal(rfc, ciec, path_params={"uuid": uuid}, periodicidad=periodicidad, periodo=periodo)


@service("sat", "declaracion-representacion", "/api/v2/sat/declaraciones/representacion/{uuid}")
def get_sat_tax_return_document(uuid: str, rfc: Optional[str] = None, ciec: Optional[str] = None,
                                periodicidad: Optional[str] = None, periodo: Optional[str] = None,
                                reset: bool = False):
    """Obtiene la representación impresa de una declaración."""
    rules.text("uuid", uuid)
    _period(periodicidad, periodo)
    return _portal(rfc, ciec, reset, {"uuid": uuid}, periodicidad=periodicidad, periodo=periodo)


@service("sat", "facturas-buscar", "/api/v2/sat/facturacion/buscar")
def search_sat_invoices(rfc: Optional[str] = None, ciec: Optional[str] = None,
                        fecha_inicial: Optional[str] = None, fecha_final: Optional[str] = None,
                        rfc_receptor: Optional[str] = None, rfc_tercero: Optional[str] = None,
                        estado_comprobante: Optional[str] = None, tipo_comprobante: Optional[str] = None,
                        complementos: Optional[List[str]] = None, uuid: Optional[str] = None):
    """Busca CFDI en el portal de facturación del SAT.

    :param fecha_inicial: ``AAAA-MM-DD``; el periodo no puede exceder 366 días.
    :param tipo_comprobante: ``I``, ``E``, ``T``, ``N`` o ``P``.
    :param complementos: filtra por estos complementos.
    """
    start = None if fecha_inicial is None else rules.date("fecha_inicial", fecha_inicial)
    end = None if fecha_final is None else rules.date("fecha_final", fecha_final)
    if start and end:
        if end < start:
            raise InvalidParameterError.of("fecha_final", "COMBINATION",
                                           "La fecha final no puede ser anterior a la inicial.")
        if (end - start).days > 366:
            raise InvalidParameterError.of("fecha_final", "RANGE",
                                           "El periodo de búsqueda no puede exceder 366 días.")
    for key, value in (("rfc_receptor", rfc_receptor), ("rfc_tercero", rfc_tercero)):
        if value is not None:
            validate_rfc(value)
    rules.optional_text("estado_comprobante", estado_comprobante)
    if tipo_comprobante is not None:
        rules.option("tipo_comprobante", tipo_comprobante, ("I", "E", "T", "N", "P"), ignore_case=True)
    if complementos is not None:
        for item in rules.items("complementos", complementos, max_items=50):
            rules.text("complementos", item, max_length=100)
    if uuid is not None:
        rules.uuid_text("uuid", uuid)
    return _portal(rfc, ciec, FechaInicialPeriodo=fecha_inicial, FechaFinalPeriodo=fecha_final,
                   RfcReceptor=rfc_receptor, RfcTercero=rfc_tercero, EstadoComprobante=estado_comprobante,
                   TipoComprobante=tipo_comprobante, Complementos=complementos,
                   FiltroComplementos=1 if complementos else None, Uuid=uuid)


@service("sat", "facturas-descargar", "/api/v2/sat/facturacion/descargar")
def download_sat_invoice(uuid: str, blob_path: str, rfc: Optional[str] = None, ciec: Optional[str] = None,
                         formato: Optional[str] = None, rfc_emisor: Optional[str] = None, reset: bool = False):
    """Descarga un CFDI.

    :param blob_path: URL del documento que devuelve la búsqueda.
    :param formato: ``xml``, ``pdf`` o ``ambos``.
    """
    rules.uuid_text("uuid", uuid)
    rules.https_url("blob_path", blob_path, max_length=2000)
    if formato is not None:
        rules.option("formato", formato, ("xml", "pdf", "ambos"))
    if rfc_emisor is not None:
        validate_rfc(rfc_emisor)
    return _portal(rfc, ciec, reset, uuid=uuid, blob_path=blob_path, formato=formato, rfc_emisor=rfc_emisor)


@service("sat", "facturacion-perfil", "/api/v2/sat/facturacion/perfil")
def get_sat_billing_profile(rfc: Optional[str] = None, ciec: Optional[str] = None, reset: bool = False):
    """Consulta el perfil de facturación."""
    return _portal(rfc, ciec, reset)


@service("sat", "opinion-cumplimiento", "/api/v2/sat/opinion-cumplimiento")
def get_sat_compliance_opinion(rfc: Optional[str] = None, ciec: Optional[str] = None, reset: bool = False):
    """Obtiene la opinión de cumplimiento (32-D)."""
    return _portal(rfc, ciec, reset)


@service("sat", "certificados-efirma", "/api/v2/sat/certificados/efirma")
def get_sat_efirma_certificates(rfc: Optional[str] = None, ciec: Optional[str] = None, reset: bool = False):
    """Lista los certificados de e.firma."""
    return _portal(rfc, ciec, reset)


@service("sat", "certificados-sello-digital", "/api/v2/sat/certificados/sello-digital")
def get_sat_seal_certificates(rfc: Optional[str] = None, ciec: Optional[str] = None, reset: bool = False):
    """Lista los certificados de sello digital."""
    return _portal(rfc, ciec, reset)
