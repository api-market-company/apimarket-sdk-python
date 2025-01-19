from __future__ import annotations
import datetime
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union
import dateparser

@dataclass
class HistorialLaboralPostResponse_data_historialLaboral_movimientos(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The fechaMovimiento property
    fecha_movimiento: Optional[datetime.date] = None
    # The salarioBase property
    salario_base: Optional[float] = None
    # The tipoDeMovimiento property
    tipo_de_movimiento: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> HistorialLaboralPostResponse_data_historialLaboral_movimientos:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: HistorialLaboralPostResponse_data_historialLaboral_movimientos
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return HistorialLaboralPostResponse_data_historialLaboral_movimientos()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        fields: Dict[str, Callable[[Any], None]] = {
            "fechaMovimiento": lambda n : setattr(self, 'fecha_movimiento', dateparser.parse(n.get_str_value())),
            "salarioBase": lambda n : setattr(self, 'salario_base', n.get_float_value()),
            "tipoDeMovimiento": lambda n : setattr(self, 'tipo_de_movimiento', n.get_str_value()),
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
        writer.write_date_value("fechaMovimiento", self.fecha_movimiento)
        writer.write_float_value("salarioBase", self.salario_base)
        writer.write_str_value("tipoDeMovimiento", self.tipo_de_movimiento)
        writer.write_additional_data_value(self.additional_data)
    

