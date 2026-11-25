from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .buscar_nacimiento_post_response_data_datos_padres import BuscarNacimientoPostResponseDataDatosPadres

@dataclass
class BuscarNacimientoPostResponseData(AdditionalDataHolder, Parsable):
    additional_data: Dict[str, Any] = field(default_factory=dict)
    curp: Optional[str] = None
    nacionalidad: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    cadena: Optional[str] = None
    nombre: Optional[str] = None
    primer_apellido: Optional[str] = None
    segundo_apellido: Optional[str] = None
    sexo: Optional[str] = None
    vivo_muerto: Optional[str] = None
    datos_padres: Optional[BuscarNacimientoPostResponseDataDatosPadres] = None

    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> BuscarNacimientoPostResponseData:
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return BuscarNacimientoPostResponseData()

    def get_field_deserializers(self) -> Dict[str, Callable[[ParseNode], None]]:
        from .buscar_nacimiento_post_response_data_datos_padres import BuscarNacimientoPostResponseDataDatosPadres
        return {
            "curp":            lambda n: setattr(self, 'curp', n.get_str_value()),
            "nacionalidad":    lambda n: setattr(self, 'nacionalidad', n.get_str_value()),
            "fechaNacimiento": lambda n: setattr(self, 'fecha_nacimiento', n.get_str_value()),
            "cadena":          lambda n: setattr(self, 'cadena', n.get_str_value()),
            "nombre":          lambda n: setattr(self, 'nombre', n.get_str_value()),
            "primerApellido":  lambda n: setattr(self, 'primer_apellido', n.get_str_value()),
            "segundoApellido": lambda n: setattr(self, 'segundo_apellido', n.get_str_value()),
            "sexo":            lambda n: setattr(self, 'sexo', n.get_str_value()),
            "vivoMuerto":      lambda n: setattr(self, 'vivo_muerto', n.get_str_value()),
            "DatosPadres":     lambda n: setattr(self, 'datos_padres', n.get_object_value(BuscarNacimientoPostResponseDataDatosPadres)),
        }

    def serialize(self, writer: SerializationWriter) -> None:
        if not writer:
            raise TypeError("writer cannot be null.")
        writer.write_str_value("curp", self.curp)
        writer.write_str_value("nacionalidad", self.nacionalidad)
        writer.write_str_value("fechaNacimiento", self.fecha_nacimiento)
        writer.write_str_value("cadena", self.cadena)
        writer.write_str_value("nombre", self.nombre)
        writer.write_str_value("primerApellido", self.primer_apellido)
        writer.write_str_value("segundoApellido", self.segundo_apellido)
        writer.write_str_value("sexo", self.sexo)
        writer.write_str_value("vivoMuerto", self.vivo_muerto)
        writer.write_object_value("DatosPadres", self.datos_padres)
        writer.write_additional_data_value(self.additional_data)
