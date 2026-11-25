"""Llama a cada función con muchos datos inválidos, sin enviar nada, y reúne los errores que produce."""
import io
import tempfile

from kink import di

import apimarket
from apimarket.validations import ValidationError

from arguments import VALID, signature
from cases import CURP, MOVEMENT, NSS, RESOURCE, UUID

CREDENTIALS = {"userId": "u", "password": "p", "certificate": "c", "privateKey": "k"}
VALUES = [None, "", " ", "x", "abc", "1", "123", "13", "x" * 3000, 5, -1, 0, 10 ** 6, True, 1.5, [], {}, [None],
          [""], ["x" * 200], ["x"] * 101, [5], [{}], {"a": {"mayor": 1}}, {"a": [1]}, b"", b"texto", b"\x00",
          b"{}", "/no/existe", ".", "..", "no-es-uuid", "2024-99-99", "http://example.com", "https://",
          "a@b", "0000000000"]


def _movements():
    complete = {**MOVEMENT, "salarioDiarioIntegrado": 250.5, "tipoDeSalario": "0", "jornada": "0", "umf": "001",
                "tipoDeTrabajador": "1", "apellidoMaterno": "LOPEZ", "claveDelTrabajador": "A1", "curp": CURP}
    for kind in ("2", "7", "8"):
        for key in complete:
            for value in VALUES:
                yield "idse_capture_movements", {"movimientos": [{**complete, "tipoDeMovimiento": kind, key: value}]}


def _nested():
    yield from _movements()
    for name in ("idse_capture_movements", "idse_get_movements_status", "idse_get_employer_registrations"):
        for key in CREDENTIALS:
            for value in [*VALUES, "ñ"]:
                yield name, {"credentials": {**CREDENTIALS, key: value}}
    for value in VALUES:
        for key in ("filename", "title", "correlation_id", "metadata"):
            yield "generate_from_template", {"options": {key: value}}
        for key in RESOURCE:
            yield "smart_processing_plan", {"resources": [{**RESOURCE, key: value}]}
        yield "get_dataset_rows", {"filter": {"a": value}}
        yield "get_dataset_rows", {"filter": {"a": {"like": value}}}
        yield "get_dataset_rows", {"filter": {value if isinstance(value, str) else "a": "1"}}


def _combinations():
    yield "get_sat_tax_returns", {"periodicidad": None, "periodo": "3"}
    yield "get_sat_tax_returns", {"periodicidad": "M", "periodo": None}
    for period in ("1", "99", "abc"):
        yield "get_sat_tax_returns", {"periodicidad": "Y", "periodo": period}
    yield "search_sat_invoices", {"fecha_inicial": "2024-02-01", "fecha_final": "2024-01-01"}
    yield "search_sat_invoices", {"fecha_inicial": "2020-01-01", "fecha_final": "2024-01-01"}
    yield "get_vehicle_owner", {"placas": None, "numero_serie": None}
    yield "search_sat_lista69b", {"rfc": None, "nombre_contribuyente": None}


def _calls(directory):
    files = [directory, io.StringIO("texto"), b"%PDF-" + b"0" * (20 * 1024 * 1024)]
    for name in VALID:
        for parameter in signature(name):
            for value in VALUES:
                yield name, {parameter: value}
    for name, parameter in [("ocr_id", "anverso"), ("ocr_id", "reverso"), ("parse_csf", "csf"),
                            ("create_template", "template"), ("update_template", "template"),
                            ("smart_processing_upload", "data"), ("verify_sat_signature", "certificate"),
                            ("verify_sat_signature", "privateKey")]:
        for value in files:
            yield name, {parameter: value}
    yield from _nested()
    yield from _combinations()


def run():
    """Devuelve ({código: (función, cambios, error)}, [errores que no son de validación])."""
    found, unexpected = {}, []
    original = apimarket.choice_process_scheduler
    apimarket.assemble()
    di["API_MARKET_API_KEY"] = "llave-de-prueba"
    # Si los datos pasan la validación, la petición se descarta aquí.
    apimarket.choice_process_scheduler = lambda function: lambda: "enviada"
    try:
        with tempfile.TemporaryDirectory() as directory:
            for name, changes in _calls(directory):
                try:
                    getattr(apimarket, name)(**{**VALID[name], **changes})
                except ValidationError as error:
                    found.setdefault(error.code, (name, changes, error))
                except Exception as error:
                    unexpected.append((name, changes, f"{type(error).__name__}: {error}"))
    finally:
        apimarket.choice_process_scheduler = original
        apimarket.assemble()
    return found, unexpected
