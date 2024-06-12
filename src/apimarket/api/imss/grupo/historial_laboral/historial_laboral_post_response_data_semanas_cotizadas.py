from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

@dataclass
class HistorialLaboralPostResponse_data_semanasCotizadas(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The semanasCotizadas property
    semanas_cotizadas: Optional[str] = None
    # The semanasDescontadas property
    semanas_descontadas: Optional[str] = None
    # The semanasReintegradas property
    semanas_reintegradas: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> HistorialLaboralPostResponse_data_semanasCotizadas:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: HistorialLaboralPostResponse_data_semanasCotizadas
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return HistorialLaboralPostResponse_data_semanasCotizadas()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        fields: Dict[str, Callable[[Any], None]] = {
            "semanasCotizadas": lambda n : setattr(self, 'semanas_cotizadas', n.get_str_value()),
            "semanasDescontadas": lambda n : setattr(self, 'semanas_descontadas', n.get_str_value()),
            "semanasReintegradas": lambda n : setattr(self, 'semanas_reintegradas', n.get_str_value()),
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
        writer.write_str_value("semanasCotizadas", self.semanas_cotizadas)
        writer.write_str_value("semanasDescontadas", self.semanas_descontadas)
        writer.write_str_value("semanasReintegradas", self.semanas_reintegradas)
        writer.write_additional_data_value(self.additional_data)
    

