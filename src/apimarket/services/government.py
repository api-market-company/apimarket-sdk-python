"""Servicios de RENAPO, REPUVE y SEP."""
from typing import Optional

from apimarket import rules
from apimarket.services._core import Call, reset_header, service
from apimarket.validations import InvalidParameterError, validate_curp


@service("renapo", "acta-nacimiento", "/api/renapo/grupo/obtener-acta-de-nacimiento")
def get_birth_certificate(curp: str, reset: bool = False):
    """Obtiene el acta de nacimiento por CURP."""
    validate_curp(curp)
    return Call(query={"curp": curp}, headers=reset_header(reset))


def _vehicle(numero_serie: Optional[str], placas: Optional[str]) -> Call:
    rules.optional_text("numero_serie", numero_serie, max_length=50)
    rules.optional_text("placas", placas, max_length=10)
    if not numero_serie and not placas:
        raise InvalidParameterError.of("numero_serie, placas", "MISSING", "Indique 'numero_serie' o 'placas'.")
    return Call(query={"numero_serie": numero_serie, "placas": placas})


@service("repuve", "propietario", "/api/repuve/grupo/consulta-propietario")
def get_vehicle_owner(numero_serie: Optional[str] = None, placas: Optional[str] = None):
    """Consulta el propietario de un vehículo por número de serie o placas."""
    return _vehicle(numero_serie, placas)


@service("repuve", "vehiculo", "/api/repuve/grupo/datos-vehiculo")
def get_vehicle_data(numero_serie: Optional[str] = None, placas: Optional[str] = None):
    """Consulta los datos de un vehículo por número de serie o placas."""
    return _vehicle(numero_serie, placas)


@service("repuve", "robo", "/api/repuve/grupo/consulta-robo")
def check_vehicle_theft(numero_serie: Optional[str] = None, placas: Optional[str] = None):
    """Consulta si un vehículo tiene reporte de robo."""
    return _vehicle(numero_serie, placas)


@service("sep", "constancia-profesional", "/api/sep/grupo/descargar-constancia-profesional")
def download_sep_professional_record(curp: str):
    """Descarga la constancia profesional de la SEP por CURP."""
    validate_curp(curp)
    return Call(query={"curp": curp})
