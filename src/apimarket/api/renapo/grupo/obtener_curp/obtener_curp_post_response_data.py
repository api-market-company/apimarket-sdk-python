from __future__ import annotations
import datetime
from dataclasses import dataclass, field

import dateparser
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

@dataclass
class ObtenerCurpPostResponse_data(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The apellidoMaterno property
    apellido_materno: Optional[str] = None
    # The apellidoPaterno property
    apellido_paterno: Optional[str] = None
    # The curp property
    curp: Optional[str] = None
    # The fechaNacimiento property
    fecha_nacimiento: Optional[datetime.date] = None
    # The mensaje property
    mensaje: Optional[str] = None
    # The nombres property
    nombres: Optional[str] = None
    # The sexo property
    sexo: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ObtenerCurpPostResponse_data:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ObtenerCurpPostResponse_data
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return ObtenerCurpPostResponse_data()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        fields: Dict[str, Callable[[Any], None]] = {
            "apellidoMaterno": lambda n : setattr(self, 'apellido_materno', n.get_str_value()),
            "apellidoPaterno": lambda n : setattr(self, 'apellido_paterno', n.get_str_value()),
            "curp": lambda n : setattr(self, 'curp', n.get_str_value()),
            "fechaNacimiento": lambda n : setattr(self, 'fecha_nacimiento', dateparser.parse(n.get_str_value())),
            "mensaje": lambda n : setattr(self, 'mensaje', n.get_str_value()),
            "nombres": lambda n : setattr(self, 'nombres', n.get_str_value()),
            "sexo": lambda n : setattr(self, 'sexo', n.get_str_value()),
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
        writer.write_str_value("apellidoMaterno", self.apellido_materno)
        writer.write_str_value("apellidoPaterno", self.apellido_paterno)
        writer.write_str_value("curp", self.curp)
        writer.write_date_value("fechaNacimiento", self.fecha_nacimiento)
        writer.write_str_value("mensaje", self.mensaje)
        writer.write_str_value("nombres", self.nombres)
        writer.write_str_value("sexo", self.sexo)
        writer.write_additional_data_value(self.additional_data)
    

