from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.api_error import APIError
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, Optional


@dataclass
class ListarCertificados400Error(APIError):
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # Código de validación único para la solicitud
    codigo_validacion: Optional[str] = None
    # Mensaje descriptivo del resultado
    message: Optional[str] = None
    # Código de estado HTTP
    status: Optional[int] = None
    # Indica si la solicitud fue exitosa
    success: Optional[bool] = None

    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ListarCertificados400Error:
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return ListarCertificados400Error()

    def get_field_deserializers(self) -> Dict[str, Callable[[ParseNode], None]]:
        return {}

    def serialize(self, writer: SerializationWriter) -> None:
        if not writer:
            raise TypeError("writer cannot be null.")
        writer.write_str_value("codigoValidacion", self.codigo_validacion)
        writer.write_str_value("message", self.message)
        writer.write_int_value("status", self.status)
        writer.write_bool_value("success", self.success)
        writer.write_additional_data_value(self.additional_data)

    @property
    def primary_message(self) -> str:
        return super().message
