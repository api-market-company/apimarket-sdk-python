from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

@dataclass
class ObtenerDatosPostResponse_codigosPostales(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The clave property
    clave: Optional[str] = None
    # The esMatriz property
    es_matriz: Optional[bool] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ObtenerDatosPostResponse_codigosPostales:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ObtenerDatosPostResponse_codigosPostales
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return ObtenerDatosPostResponse_codigosPostales()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        fields: Dict[str, Callable[[Any], None]] = {
            "clave": lambda n : setattr(self, 'clave', n.get_str_value()),
            "esMatriz": lambda n : setattr(self, 'es_matriz', n.get_bool_value()),
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
        writer.write_str_value("clave", self.clave)
        writer.write_bool_value("esMatriz", self.es_matriz)
        writer.write_additional_data_value(self.additional_data)
    

