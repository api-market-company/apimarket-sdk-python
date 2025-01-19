from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

@dataclass
class ObtenerDatosIdcifPostResponse_data(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # Identificador de la Constancia de Situación Fiscal
    idcif: Optional[str] = None
    # Nombre
    nombre: Optional[str] = None
    # Razon social
    razon_social: Optional[str] = None
    # Regimen capital
    regimen_capital: Optional[str] = None
    # Registro Federal de Contribuyentes
    rfc: Optional[str] = None
    # Tipo de persona
    tipo_persona: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ObtenerDatosIdcifPostResponse_data:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ObtenerDatosIdcifPostResponse_data
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return ObtenerDatosIdcifPostResponse_data()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        fields: Dict[str, Callable[[Any], None]] = {
            "idcif": lambda n : setattr(self, 'idcif', n.get_str_value()),
            "nombre": lambda n : setattr(self, 'nombre', n.get_str_value()),
            "razon_social": lambda n : setattr(self, 'razon_social', n.get_str_value()),
            "regimen_capital": lambda n : setattr(self, 'regimen_capital', n.get_str_value()),
            "rfc": lambda n : setattr(self, 'rfc', n.get_str_value()),
            "tipo_persona": lambda n : setattr(self, 'tipo_persona', n.get_str_value()),
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
        writer.write_str_value("idcif", self.idcif)
        writer.write_str_value("nombre", self.nombre)
        writer.write_str_value("razon_social", self.razon_social)
        writer.write_str_value("regimen_capital", self.regimen_capital)
        writer.write_str_value("rfc", self.rfc)
        writer.write_str_value("tipo_persona", self.tipo_persona)
        writer.write_additional_data_value(self.additional_data)
    

