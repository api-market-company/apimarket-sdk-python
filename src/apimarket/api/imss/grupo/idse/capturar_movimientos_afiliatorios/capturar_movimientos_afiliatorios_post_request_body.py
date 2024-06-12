from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .capturar_movimientos_afiliatorios_post_request_body_movimientos import CapturarMovimientosAfiliatoriosPostRequestBody_movimientos

@dataclass
class CapturarMovimientosAfiliatoriosPostRequestBody(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The movimientos property
    movimientos: Optional[List[CapturarMovimientosAfiliatoriosPostRequestBody_movimientos]] = None
    # Please provide a valid URL format. Here, we provide you with the IDSE response to confirm your request.
    webhook: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> CapturarMovimientosAfiliatoriosPostRequestBody:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: CapturarMovimientosAfiliatoriosPostRequestBody
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return CapturarMovimientosAfiliatoriosPostRequestBody()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .capturar_movimientos_afiliatorios_post_request_body_movimientos import CapturarMovimientosAfiliatoriosPostRequestBody_movimientos

        from .capturar_movimientos_afiliatorios_post_request_body_movimientos import CapturarMovimientosAfiliatoriosPostRequestBody_movimientos

        fields: Dict[str, Callable[[Any], None]] = {
            "movimientos": lambda n : setattr(self, 'movimientos', n.get_collection_of_object_values(CapturarMovimientosAfiliatoriosPostRequestBody_movimientos)),
            "webhook": lambda n : setattr(self, 'webhook', n.get_str_value()),
        }
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if not writer:
            raise TypeError("writer cannot be null.")
        writer.write_collection_of_object_values("movimientos", self.movimientos)
        writer.write_str_value("webhook", self.webhook)
        writer.write_additional_data_value(self.additional_data)
    

