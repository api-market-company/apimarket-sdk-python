from __future__ import annotations
import datetime
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

@dataclass
class CodigosPostales(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The admin_code1 property
    admin_code1: Optional[str] = None
    # The admin_code2 property
    admin_code2: Optional[str] = None
    # The admin_code3 property
    admin_code3: Optional[str] = None
    # The admin_name1 property
    admin_name1: Optional[str] = None
    # The admin_name2 property
    admin_name2: Optional[str] = None
    # The admin_name3 property
    admin_name3: Optional[str] = None
    # The country_code property
    country_code: Optional[str] = None
    # The id property
    id: Optional[int] = None
    # The place_name property
    place_name: Optional[str] = None
    # The postal_code property
    postal_code: Optional[str] = None
    # The updated_at property
    updated_at: Optional[datetime.datetime] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> CodigosPostales:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: CodigosPostales
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return CodigosPostales()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        fields: Dict[str, Callable[[Any], None]] = {
            "admin_code1": lambda n : setattr(self, 'admin_code1', n.get_str_value()),
            "admin_code2": lambda n : setattr(self, 'admin_code2', n.get_str_value()),
            "admin_code3": lambda n : setattr(self, 'admin_code3', n.get_str_value()),
            "admin_name1": lambda n : setattr(self, 'admin_name1', n.get_str_value()),
            "admin_name2": lambda n : setattr(self, 'admin_name2', n.get_str_value()),
            "admin_name3": lambda n : setattr(self, 'admin_name3', n.get_str_value()),
            "country_code": lambda n : setattr(self, 'country_code', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "place_name": lambda n : setattr(self, 'place_name', n.get_str_value()),
            "postal_code": lambda n : setattr(self, 'postal_code', n.get_str_value()),
            "updated_at": lambda n : setattr(self, 'updated_at', n.get_datetime_value()),
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
        writer.write_str_value("admin_code1", self.admin_code1)
        writer.write_str_value("admin_code2", self.admin_code2)
        writer.write_str_value("admin_code3", self.admin_code3)
        writer.write_str_value("admin_name1", self.admin_name1)
        writer.write_str_value("admin_name2", self.admin_name2)
        writer.write_str_value("admin_name3", self.admin_name3)
        writer.write_str_value("country_code", self.country_code)
        writer.write_int_value("id", self.id)
        writer.write_str_value("place_name", self.place_name)
        writer.write_str_value("postal_code", self.postal_code)
        writer.write_datetime_value("updated_at", self.updated_at)
        writer.write_additional_data_value(self.additional_data)
    

