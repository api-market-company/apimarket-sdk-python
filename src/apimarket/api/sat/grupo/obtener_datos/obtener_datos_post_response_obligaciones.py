from __future__ import annotations
import datetime
from dataclasses import dataclass, field

import dateparser
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

@dataclass
class ObtenerDatosPostResponse_obligaciones(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The cobligacion property
    cobligacion: Optional[str] = None
    # The cvePago property
    cve_pago: Optional[str] = None
    # The dobligLc property
    doblig_lc: Optional[str] = None
    # The dobligacion property
    dobligacion: Optional[str] = None
    # The faltaOblig property
    falta_oblig: Optional[datetime.date] = None
    # The fbajaOblig property
    fbaja_oblig: Optional[str] = None
    # The fefecAOblig property
    fefec_a_oblig: Optional[datetime.date] = None
    # The fefecBOblig property
    fefec_b_oblig: Optional[str] = None
    # The ffinLegal property
    ffin_legal: Optional[str] = None
    # The finiLegal property
    fini_legal: Optional[datetime.date] = None
    # The tcontribucion property
    tcontribucion: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ObtenerDatosPostResponse_obligaciones:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ObtenerDatosPostResponse_obligaciones
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return ObtenerDatosPostResponse_obligaciones()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        fields: Dict[str, Callable[[Any], None]] = {
            "cobligacion": lambda n : setattr(self, 'cobligacion', n.get_str_value()),
            "cvePago": lambda n : setattr(self, 'cve_pago', n.get_str_value()),
            "dobligLc": lambda n : setattr(self, 'doblig_lc', n.get_str_value()),
            "dobligacion": lambda n : setattr(self, 'dobligacion', n.get_str_value()),
            "faltaOblig": lambda n : setattr(self, 'falta_oblig', dateparser.parse(n.get_str_value())),
            "fbajaOblig": lambda n : setattr(self, 'fbaja_oblig', n.get_str_value()),
            "fefecAOblig": lambda n : setattr(self, 'fefec_a_oblig', dateparser.parse(n.get_str_value())),
            "fefecBOblig": lambda n : setattr(self, 'fefec_b_oblig', n.get_str_value()),
            "ffinLegal": lambda n : setattr(self, 'ffin_legal', n.get_str_value()),
            "finiLegal": lambda n : setattr(self, 'fini_legal', dateparser.parse(n.get_str_value())),
            "tcontribucion": lambda n : setattr(self, 'tcontribucion', n.get_str_value()),
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
        writer.write_str_value("cobligacion", self.cobligacion)
        writer.write_str_value("cvePago", self.cve_pago)
        writer.write_str_value("dobligLc", self.doblig_lc)
        writer.write_str_value("dobligacion", self.dobligacion)
        writer.write_date_value("faltaOblig", self.falta_oblig)
        writer.write_str_value("fbajaOblig", self.fbaja_oblig)
        writer.write_date_value("fefecAOblig", self.fefec_a_oblig)
        writer.write_str_value("fefecBOblig", self.fefec_b_oblig)
        writer.write_str_value("ffinLegal", self.ffin_legal)
        writer.write_date_value("finiLegal", self.fini_legal)
        writer.write_str_value("tcontribucion", self.tcontribucion)
        writer.write_additional_data_value(self.additional_data)
    

