from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, Optional

@dataclass
class BuscarNacimientoPostResponseDataDatosPadres(AdditionalDataHolder, Parsable):
    additional_data: Dict[str, Any] = field(default_factory=dict)
    curp_padre: Optional[str] = None
    nombre_padre: Optional[str] = None
    primer_apellido_padre: Optional[str] = None
    segundo_apellido_padre: Optional[str] = None
    nacionalidad_padre: Optional[str] = None
    curp_madre: Optional[str] = None
    nombre_madre: Optional[str] = None
    primer_apellido_madre: Optional[str] = None
    segundo_apellido_madre: Optional[str] = None
    nacionalidad_madre: Optional[str] = None

    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> BuscarNacimientoPostResponseDataDatosPadres:
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return BuscarNacimientoPostResponseDataDatosPadres()

    def get_field_deserializers(self) -> Dict[str, Callable[[ParseNode], None]]:
        return {
            "curpPADRE":             lambda n: setattr(self, 'curp_padre', n.get_str_value()),
            "NombrePadre":           lambda n: setattr(self, 'nombre_padre', n.get_str_value()),
            "PrimerApellidoPadre":   lambda n: setattr(self, 'primer_apellido_padre', n.get_str_value()),
            "SegundoApellidoPadre":  lambda n: setattr(self, 'segundo_apellido_padre', n.get_str_value()),
            "NacionalidadPadre":     lambda n: setattr(self, 'nacionalidad_padre', n.get_str_value()),
            "curpMADRE":             lambda n: setattr(self, 'curp_madre', n.get_str_value()),
            "NombreMadre":           lambda n: setattr(self, 'nombre_madre', n.get_str_value()),
            "PrimerApellidoMadre":   lambda n: setattr(self, 'primer_apellido_madre', n.get_str_value()),
            "SegundoApellidoMadre":  lambda n: setattr(self, 'segundo_apellido_madre', n.get_str_value()),
            "NacionalidadMadre":     lambda n: setattr(self, 'nacionalidad_madre', n.get_str_value()),
        }

    def serialize(self, writer: SerializationWriter) -> None:
        if not writer:
            raise TypeError("writer cannot be null.")
        writer.write_str_value("curpPADRE", self.curp_padre)
        writer.write_str_value("NombrePadre", self.nombre_padre)
        writer.write_str_value("PrimerApellidoPadre", self.primer_apellido_padre)
        writer.write_str_value("SegundoApellidoPadre", self.segundo_apellido_padre)
        writer.write_str_value("NacionalidadPadre", self.nacionalidad_padre)
        writer.write_str_value("curpMADRE", self.curp_madre)
        writer.write_str_value("NombreMadre", self.nombre_madre)
        writer.write_str_value("PrimerApellidoMadre", self.primer_apellido_madre)
        writer.write_str_value("SegundoApellidoMadre", self.segundo_apellido_madre)
        writer.write_str_value("NacionalidadMadre", self.nacionalidad_madre)
        writer.write_additional_data_value(self.additional_data)
