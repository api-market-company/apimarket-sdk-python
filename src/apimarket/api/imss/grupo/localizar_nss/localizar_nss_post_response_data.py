from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, Optional


@dataclass
class LocalizarNssPostResponseData(AdditionalDataHolder, Parsable):
    additional_data: Dict[str, Any] = field(default_factory=dict)
    curp: Optional[str] = None
    nss: Optional[str] = None
    nombre: Optional[str] = None
    apaterno: Optional[str] = None
    amaterno: Optional[str] = None
    fec_nacimiento: Optional[str] = None
    sexo: Optional[str] = None

    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> LocalizarNssPostResponseData:
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return LocalizarNssPostResponseData()

    def get_field_deserializers(self) -> Dict[str, Callable[[ParseNode], None]]:
        return {
            "curp":           lambda n: setattr(self, 'curp', n.get_str_value()),
            "nss":            lambda n: setattr(self, 'nss', n.get_str_value()),
            "nombre":         lambda n: setattr(self, 'nombre', n.get_str_value()),
            "apaterno":       lambda n: setattr(self, 'apaterno', n.get_str_value()),
            "amaterno":       lambda n: setattr(self, 'amaterno', n.get_str_value()),
            "fecNacimiento":  lambda n: setattr(self, 'fec_nacimiento', n.get_str_value()),
            "sexo":           lambda n: setattr(self, 'sexo', n.get_str_value()),
        }

    def serialize(self, writer: SerializationWriter) -> None:
        if not writer:
            raise TypeError("writer cannot be null.")
        writer.write_str_value("curp", self.curp)
        writer.write_str_value("nss", self.nss)
        writer.write_str_value("nombre", self.nombre)
        writer.write_str_value("apaterno", self.apaterno)
        writer.write_str_value("amaterno", self.amaterno)
        writer.write_str_value("fecNacimiento", self.fec_nacimiento)
        writer.write_str_value("sexo", self.sexo)
        writer.write_additional_data_value(self.additional_data)
