from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, Optional


@dataclass
class ValidarDatosPostResponseData(AdditionalDataHolder, Parsable):
    additional_data: Dict[str, Any] = field(default_factory=dict)
    resultado: Optional[str] = None

    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ValidarDatosPostResponseData:
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return ValidarDatosPostResponseData()

    def get_field_deserializers(self) -> Dict[str, Callable[[ParseNode], None]]:
        return {
            "resultado": lambda n: setattr(self, 'resultado', n.get_str_value()),
        }

    def serialize(self, writer: SerializationWriter) -> None:
        if not writer:
            raise TypeError("writer cannot be null.")
        writer.write_str_value("resultado", self.resultado)
        writer.write_additional_data_value(self.additional_data)
