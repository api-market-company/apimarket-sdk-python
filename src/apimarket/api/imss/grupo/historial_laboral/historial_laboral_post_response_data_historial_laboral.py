from __future__ import annotations
import datetime
from dataclasses import dataclass, field

import dateparser
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union


@dataclass
class HistorialLaboralPostResponse_data_historialLaboral(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The entidadFederativa property
    entidad_federativa: Optional[str] = None
    # The fechaAlta property
    fecha_alta: Optional[datetime.date] = None
    # The fechaBaja property
    fecha_baja: Optional[datetime.date] = None
    # The nombrePatron property
    nombre_patron: Optional[str] = None
    # The registroPatronal property
    registro_patronal: Optional[str] = None
    # The salarioBaseCotizacion property
    salario_base_cotizacion: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> HistorialLaboralPostResponse_data_historialLaboral:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: HistorialLaboralPostResponse_data_historialLaboral
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return HistorialLaboralPostResponse_data_historialLaboral()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        fields: Dict[str, Callable[[Any], None]] = {
            "entidadFederativa": lambda n : setattr(self, 'entidad_federativa', n.get_str_value()),
            "fechaAlta": lambda n : setattr(self, 'fecha_alta', dateparser.parse(n.get_str_value())),
            "fechaBaja": lambda n : setattr(self, 'fecha_baja', dateparser.parse(n.get_str_value())),
            "nombrePatron": lambda n : setattr(self, 'nombre_patron', n.get_str_value()),
            "registroPatronal": lambda n : setattr(self, 'registro_patronal', n.get_str_value()),
            "salarioBaseCotizacion": lambda n : setattr(self, 'salario_base_cotizacion', n.get_str_value()),
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
        writer.write_str_value("entidadFederativa", self.entidad_federativa)
        writer.write_date_value("fechaAlta", self.fecha_alta)
        writer.write_date_value("fechaBaja", self.fecha_baja)
        writer.write_str_value("nombrePatron", self.nombre_patron)
        writer.write_str_value("registroPatronal", self.registro_patronal)
        writer.write_str_value("salarioBaseCotizacion", self.salario_base_cotizacion)
        writer.write_additional_data_value(self.additional_data)
    

