from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

@dataclass
class CalcularRfcPostResponseData(AdditionalDataHolder, Parsable):
    additional_data: Dict[str, Any] = field(default_factory=dict)
    rfc: Optional[str] = None
    nombres: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    mensaje: Optional[str] = None

    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> CalcularRfcPostResponseData:
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return CalcularRfcPostResponseData()

    def get_field_deserializers(self) -> Dict[str, Callable[[ParseNode], None]]:
        return {
            "rfc":             lambda n: setattr(self, 'rfc', n.get_str_value()),
            "nombres":         lambda n: setattr(self, 'nombres', n.get_str_value()),
            "apellidoPaterno": lambda n: setattr(self, 'apellido_paterno', n.get_str_value()),
            "apellidoMaterno": lambda n: setattr(self, 'apellido_materno', n.get_str_value()),
            "fechaNacimiento": lambda n: setattr(self, 'fecha_nacimiento', n.get_str_value()),
            "mensaje":         lambda n: setattr(self, 'mensaje', n.get_str_value()),
        }

    def serialize(self, writer: SerializationWriter) -> None:
        if not writer:
            raise TypeError("writer cannot be null.")
        writer.write_str_value("rfc", self.rfc)
        writer.write_str_value("nombres", self.nombres)
        writer.write_str_value("apellidoPaterno", self.apellido_paterno)
        writer.write_str_value("apellidoMaterno", self.apellido_materno)
        writer.write_str_value("fechaNacimiento", self.fecha_nacimiento)
        writer.write_str_value("mensaje", self.mensaje)
        writer.write_additional_data_value(self.additional_data)
