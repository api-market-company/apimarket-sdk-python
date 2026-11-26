from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .obtener_rfc_post_response_data import ObtenerRfcPostResponseData


@dataclass
class ObtenerRfcPostResponse(AdditionalDataHolder, Parsable):
    additional_data: Dict[str, Any] = field(default_factory=dict)
    codigo_validacion: Optional[str] = None
    data: Optional[ObtenerRfcPostResponseData] = None
    message: Optional[str] = None
    status: Optional[int] = None
    success: Optional[bool] = None

    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ObtenerRfcPostResponse:
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return ObtenerRfcPostResponse()

    def get_field_deserializers(self) -> Dict[str, Callable[[ParseNode], None]]:
        from .obtener_rfc_post_response_data import ObtenerRfcPostResponseData

        def _parse_data(n: ParseNode) -> None:
            # API returns [] when no RFC is found — treat as None
            try:
                result = n.get_object_value(ObtenerRfcPostResponseData)
                self.data = result if (result and result.rfc) else None
            except Exception:
                self.data = None

        return {
            "codigoValidacion": lambda n: setattr(self, 'codigo_validacion', n.get_str_value()),
            "data":             _parse_data,
            "message":          lambda n: setattr(self, 'message', n.get_str_value()),
            "status":           lambda n: setattr(self, 'status', n.get_int_value()),
            "success":          lambda n: setattr(self, 'success', n.get_bool_value()),
        }

    def serialize(self, writer: SerializationWriter) -> None:
        if not writer:
            raise TypeError("writer cannot be null.")
        writer.write_str_value("codigoValidacion", self.codigo_validacion)
        writer.write_object_value("data", self.data)
        writer.write_str_value("message", self.message)
        writer.write_int_value("status", self.status)
        writer.write_bool_value("success", self.success)
        writer.write_additional_data_value(self.additional_data)
