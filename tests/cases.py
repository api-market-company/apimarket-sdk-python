"""Petición esperada de cada servicio: (función, argumentos, petición)."""
from apimarket.services import REGISTRY

CURP = "XEXX010101MNEXXXA4"
NSS = "12345678903"
RFC = "XAXX010101000"
WEBHOOK = "https://example.com/hook"
CREDENTIALS = {"userId": RFC, "password": "p", "certificate": "c", "privateKey": "k"}
FILE = b"contenido"
PDF = b"%PDF-1.7 prueba"
TEMPLATE = b'{"schemas": [[]]}'
CSV = b"curp\nXEXX010101MNEXXXA4\n"
UUID = "550e8400-e29b-41d4-a716-446655440000"
CODE = "A" * 20
MOVEMENT = {"nss": NSS, "nombre": "JUAN", "apellidoPaterno": "PEREZ", "tipoDeMovimiento": "2",
            "causaDeBaja": "1", "fechaDeMovimiento": "31-01-2024", "registroPatronal": "A1234567890"}
RESOURCE = {"resource": "r", "field": "curp", "url": "https://example.com/s", "json_path_query": "$.data"}


def sat(path, **extra):
    return {"path": f"/api/v2/sat/{path}", "json": {"rfc": RFC, "ciec": "secreta1", **extra}}


PORTAL = {"rfc": RFC, "ciec": "secreta1"}
INFONAVIT = "/api/v2/infonavit"

# (función, argumentos, petición esperada)
CASES = [
    ("get_balance", {}, {"method": "GET", "path": "/api/balance"}),
    ("get_public_key", {}, {"method": "GET", "path": "/api/v2/apimarket/public-key"}),
    ("store_token", {"name": "n", "company": "e", "permissions": ["a"]},
     {"path": "/api/v2/apimarket/tokens", "json": {"name": "n", "empresa": "e", "permissions": ["a"]}}),
    ("search_postal_codes", {"postal_code": "eq.10001"},
     {"path": "/api/v2/codigos-postales", "query": {"postal_code": "eq.10001"}}),
    ("get_birth_certificate", {"curp": CURP},
     {"path": "/api/renapo/grupo/obtener-acta-de-nacimiento", "query": {"curp": CURP}}),
    ("get_vehicle_owner", {"placas": "ABC123"},
     {"path": "/api/repuve/grupo/consulta-propietario", "query": {"placas": "ABC123"}}),
    ("get_vehicle_data", {"numero_serie": "S1"},
     {"path": "/api/repuve/grupo/datos-vehiculo", "query": {"numero_serie": "S1"}}),
    ("check_vehicle_theft", {"placas": "ABC123"},
     {"path": "/api/repuve/grupo/consulta-robo", "query": {"placas": "ABC123"}}),
    ("download_sep_professional_record", {"curp": CURP},
     {"path": "/api/sep/grupo/descargar-constancia-profesional", "query": {"curp": CURP}}),
    ("get_imss_pension", {"nss": NSS}, {"path": "/api/imss/grupo/consultar-pension", "query": {"nss": NSS}}),
    ("get_labor_history_lite", {"curp": CURP, "email": "a@example.com"},
     {"path": "/api/imss/grupo/historial-laboral-lite", "query": {"curp": CURP, "email": "a@example.com"}}),
    ("get_rpci", {"curp": CURP}, {"path": "/api/imss/grupo/rpci", "query": {"curp": CURP}}),
    ("get_employment_trajectory", {"identificador": CURP},
     {"path": "/api/imss/grupo/trayectoria-laboral", "query": {"identificador": CURP}}),
    ("get_assigned_umf", {"nss": NSS}, {"path": "/api/imss/grupo/umf-asignada", "query": {"nss": NSS}}),
    ("get_nss_data", {"nss": NSS}, {"path": "/api/imss/grupo/obtener-datos-nss", "query": {"nss": NSS}}),
    ("idse_capture_movements", {"movimientos": [MOVEMENT], "webhook": WEBHOOK},
     {"path": "/api/imss/grupo/idse/capturar-movimientos-afiliatorios",
      "json": {"movimientos": [MOVEMENT], "webhook": WEBHOOK}}),
    ("idse_get_movements_status",
     {"lote": 7, "webhook": WEBHOOK, "credentials": CREDENTIALS, "codigo_validacion_relacionado": CODE},
     {"path": "/api/imss/grupo/idse/consultar-movimientos-afiliatorios",
      "json": {"lote": 7, "webhook": WEBHOOK, "credentials": CREDENTIALS, "codigoDeValidacionRelacionado": CODE}}),
    ("idse_get_employer_registrations", {"webhook": WEBHOOK},
     {"path": "/api/imss/grupo/idse/registros-patronales", "json": {"webhook": WEBHOOK}}),
    ("get_infonavit_technical_sheet", {"identificador": CURP},
     {"path": f"{INFONAVIT}/ficha-tecnica", "query": {"identificador": CURP}}),
    ("get_infonavit_borrower_data", {"identificador": NSS},
     {"path": f"{INFONAVIT}/datos-acreditado", "query": {"identificador": NSS}}),
    ("get_infonavit_contact_data", {"nss": NSS},
     {"path": f"{INFONAVIT}/obtener-datos-contacto", "query": {"nss": NSS}}),
    *[(name, {"num_credito": "1234567890"}, {"path": f"{INFONAVIT}/{path}", "query": {"num_credito": "1234567890"}})
      for name, path in [
          ("get_infonavit_credit_history", "historico"),
          ("get_infonavit_financial_data", "datos-financieros"),
          ("get_infonavit_collection_data", "datos-cobranza"),
          ("get_infonavit_credit_history_report", "obtener-historico-credito"),
          ("get_infonavit_account_statement", "obtener-estado-cuenta"),
          ("get_infonavit_interest_report", "obtener-reporte-intereses"),
      ]],
    ("check_sat_rfc", {"rfc": RFC}, {"path": "/api/sat/grupo/validar-rfc", "query": {"rfc": RFC}}),
    ("get_fiscal_data_by_idcif", {"rfc": RFC, "idcif": "1"},
     {"path": "/api/sat/grupo/obtener-datos-idcif", "query": {"rfc": RFC, "idcif": "1"}}),
    ("parse_csf", {"csf": PDF}, {"path": "/api/sat/grupo/parse-csf", "files": {"csf": PDF}}),
    ("get_rfc_certificates", {"rfc": RFC},
     {"path": "/api/sat/grupo/obtener-certificados-rfc", "query": {"rfc": RFC}}),
    ("validate_sat_receiver", {"rfc": RFC, "nombre": "NOMBRE", "codigo_postal": "01000", "regimen_fiscal": "601"},
     {"path": "/api/sat/grupo/validar-datos-receptor",
      "query": {"rfc": RFC, "nombre": "NOMBRE", "codigo_postal": "01000", "regimen_fiscal": "601"}}),
    ("verify_sat_signature", {"rfc": RFC, "password": "p", "certificate": FILE, "privateKey": FILE},
     {"path": "/api/sat/grupo/verificar-firma-electronica",
      "files": {"userId": RFC.encode(), "password": b"p", "certificate": FILE, "privateKey": FILE}}),
    *[(name, PORTAL, sat(path)) for name, path in [
        ("get_sat_information", "informacion"),
        ("get_sat_csf", "csf"),
        ("get_sat_cif", "cif"),
        ("get_sat_read_messages", "buzon/leidos"),
        ("get_sat_unread_messages", "buzon/nuevos"),
        ("get_sat_contact_methods", "buzon/medios-contacto"),
        ("get_sat_billing_profile", "facturacion/perfil"),
        ("get_sat_compliance_opinion", "opinion-cumplimiento"),
        ("get_sat_efirma_certificates", "certificados/efirma"),
        ("get_sat_seal_certificates", "certificados/sello-digital"),
    ]],
    ("read_sat_message", {"uuid": "u1", **PORTAL}, sat("buzon/leer/u1")),
    ("get_sat_tax_returns", {"year": 2024, "periodicidad": "M", "periodo": "3", **PORTAL},
     sat("declaraciones/2024", periodicidad="M", periodo="3")),
    ("get_sat_tax_return_receipt", {"uuid": "u1", **PORTAL}, sat("declaraciones/obtener-acuse/u1")),
    ("get_sat_tax_return_document", {"uuid": "u1", **PORTAL}, sat("declaraciones/representacion/u1")),
    ("search_sat_invoices", {"fecha_inicial": "2024-01-01", "complementos": ["pago"], **PORTAL},
     sat("facturacion/buscar", FechaInicialPeriodo="2024-01-01", Complementos=["pago"], FiltroComplementos=1)),
    ("download_sat_invoice", {"uuid": UUID, "blob_path": "https://example.com/b", **PORTAL},
     sat("facturacion/descargar", uuid=UUID, blob_path="https://example.com/b")),
    ("ocr_id", {"anverso": PDF}, {"path": "/api/ai/v2/ocr-id", "files": {"anverso": PDF}}),
    ("create_template", {"template": TEMPLATE}, {"path": "/api/ai/v2/templates", "files": {"template": TEMPLATE}}),
    ("update_template", {"template_id": "9", "template": TEMPLATE},
     {"path": "/api/ai/v2/templates/9", "files": {"_method": b"PUT", "template": TEMPLATE}}),
    ("generate_from_template", {"template_id": "9", "inputs": [{"a": "b"}]},
     {"path": "/api/ai/v2/templates/9", "json": {"inputs": [{"a": "b"}]}}),
    ("smart_processing_upload", {"data": CSV}, {"path": "/api/ai/v2/smart-processing", "files": {"data": CSV}}),
    ("smart_processing_plan", {"resources": [RESOURCE]},
     {"path": "/api/ai/v2/smart-processing/plan", "json": {"resources": [RESOURCE]}}),
    ("smart_processing_estimate", {"dataset": "d"},
     {"path": "/api/ai/v2/smart-processing/estimate", "json": {"dataset": "d"}}),
    ("smart_processing_execute", {"dataset": "d"},
     {"path": "/api/ai/v2/smart-processing/execute", "json": {"dataset": "d"}}),
    ("smart_processing_export", {"transaction_id": 3},
     {"path": "/api/ai/v2/smart-processing/export", "json": {"transaction_id": 3}}),
    ("smart_processing_status", {"transaction_id": 3},
     {"method": "GET", "path": "/api/ai/v2/smart-processing/status", "query": {"transaction_id": "3"}}),
    ("smart_processing_delete", {"resource": "d"},
     {"method": "DELETE", "path": "/api/ai/v2/smart-processing/d"}),
    ("list_datasets", {}, {"method": "GET", "path": "/api/ai/v2/dataset"}),
    ("get_dataset_rows", {"resource": "d", "filter": {"a": "1", "b": {"like": "x"}}, "per_page": 5},
     {"method": "GET", "path": "/api/ai/v2/dataset/d",
      "query": {"filter[a]": "1", "filter[b][like]": "x", "per_page": "5"}}),
    ("get_dataset_row", {"resource": "d", "row_id": 4}, {"method": "GET", "path": "/api/ai/v2/dataset/d/4"}),
]


_GROUPS = {spec.function.__name__: spec.group for spec in REGISTRY}


def cases_for(group):
    """Casos de un área, listos para ``pytest.mark.parametrize``."""
    return {"argnames": "name,arguments,expected",
            "argvalues": [case for case in CASES if _GROUPS[case[0]] == group],
            "ids": [case[0] for case in CASES if _GROUPS[case[0]] == group]}
