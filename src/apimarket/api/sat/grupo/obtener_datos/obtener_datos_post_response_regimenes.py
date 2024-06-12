from __future__ import annotations
import datetime
from dataclasses import dataclass, field

import dateparser
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

@dataclass
class ObtenerDatosPostResponse_regimenes(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The cregimen property
    cregimen: Optional[str] = None
    # The dregimen property
    dregimen: Optional[str] = None
    # The faltaReg property
    falta_reg: Optional[datetime.date] = None
    # The fbajaReg property
    fbaja_reg: Optional[str] = None
    # The fefecAReg property
    fefec_a_reg: Optional[datetime.date] = None
    # The fefecBReg property
    fefec_b_reg: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ObtenerDatosPostResponse_regimenes:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ObtenerDatosPostResponse_regimenes
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return ObtenerDatosPostResponse_regimenes()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        fields: Dict[str, Callable[[Any], None]] = {
            "cregimen": lambda n : setattr(self, 'cregimen', n.get_str_value()),
            "dregimen": lambda n : setattr(self, 'dregimen', n.get_str_value()),
            "faltaReg": lambda n : setattr(self, 'falta_reg', dateparser.parse(n.get_str_value())),
            "fbajaReg": lambda n : setattr(self, 'fbaja_reg', n.get_str_value()),
            "fefecAReg": lambda n : setattr(self, 'fefec_a_reg', dateparser.parse(n.get_str_value())),
            "fefecBReg": lambda n : setattr(self, 'fefec_b_reg', n.get_str_value()),
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
        writer.write_str_value("cregimen", self.cregimen)
        writer.write_str_value("dregimen", self.dregimen)
        writer.write_date_value("faltaReg", self.falta_reg)
        writer.write_str_value("fbajaReg", self.fbaja_reg)
        writer.write_date_value("fefecAReg", self.fefec_a_reg)
        writer.write_str_value("fefecBReg", self.fefec_b_reg)
        writer.write_additional_data_value(self.additional_data)
    

