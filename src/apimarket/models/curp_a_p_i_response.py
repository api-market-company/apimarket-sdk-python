from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .valid_c_u_r_p_user_data import ValidCURPUserData

@dataclass
class CurpAPIResponse(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The codigoValidacion property
    codigo_validacion: Optional[str] = None
    # The data property
    data: Optional[ValidCURPUserData] = None
    # The message property
    message: Optional[str] = None
    # The status property
    status: Optional[int] = None
    # The success property
    success: Optional[bool] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> CurpAPIResponse:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: CurpAPIResponse
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return CurpAPIResponse()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .valid_c_u_r_p_user_data import ValidCURPUserData

        from .valid_c_u_r_p_user_data import ValidCURPUserData

        fields: Dict[str, Callable[[Any], None]] = {
            "codigoValidacion": lambda n : setattr(self, 'codigo_validacion', n.get_str_value()),
            "data": lambda n : setattr(self, 'data', n.get_object_value(ValidCURPUserData)),
            "message": lambda n : setattr(self, 'message', n.get_str_value()),
            "status": lambda n : setattr(self, 'status', n.get_int_value()),
            "success": lambda n : setattr(self, 'success', n.get_bool_value()),
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
        writer.write_str_value("codigoValidacion", self.codigo_validacion)
        writer.write_object_value("data", self.data)
        writer.write_str_value("message", self.message)
        writer.write_int_value("status", self.status)
        writer.write_bool_value("success", self.success)
        writer.write_additional_data_value(self.additional_data)
    

