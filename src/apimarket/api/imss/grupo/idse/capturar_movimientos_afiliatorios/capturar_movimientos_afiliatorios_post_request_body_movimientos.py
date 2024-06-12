from __future__ import annotations
import datetime
from dataclasses import dataclass, field

import dateparser
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

@dataclass
class CapturarMovimientosAfiliatoriosPostRequestBody_movimientos(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The apellidoMaterno property
    apellido_materno: Optional[str] = None
    # The apellidoPaterno property
    apellido_paterno: Optional[str] = None
    # Required for 'BAJA' movimiento. Valid values are based on the reasonsForLeave array. Conditional validations apply.
    causa_de_baja: Optional[str] = None
    # The claveDelTrabajador property
    clave_del_trabajador: Optional[str] = None
    # Must be a valid CURP format.
    curp: Optional[str] = None
    # Date format should be 'd-m-Y'. Conditional date range validations apply.
    fecha_de_movimiento: Optional[datetime.date] = None
    # Required for certain types of movimiento. Valid values are based on the journalTypes array. Conditional validations apply.
    jornada: Optional[str] = None
    # The nombre property
    nombre: Optional[str] = None
    # Must be a valid NSS format.
    nss: Optional[str] = None
    # The registroPatronal property
    registro_patronal: Optional[str] = None
    # Required for certain types of movimiento. Conditional validations apply.
    salario_diario_integrado: Optional[float] = None
    # Valid values are based on the kindOfMovements array. Conditional validations apply.
    tipo_de_movimiento: Optional[str] = None
    # Required for certain types of movimiento. Valid values are based on the salarioTypes array. Conditional validations apply.
    tipo_de_salario: Optional[str] = None
    # Required for 'REINGRESO'. Conditional validations apply.
    tipo_de_trabajador: Optional[str] = None
    # Required for certain types of movimiento. Conditional validations apply.
    umf: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> CapturarMovimientosAfiliatoriosPostRequestBody_movimientos:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: CapturarMovimientosAfiliatoriosPostRequestBody_movimientos
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return CapturarMovimientosAfiliatoriosPostRequestBody_movimientos()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        fields: Dict[str, Callable[[Any], None]] = {
            "apellidoMaterno": lambda n : setattr(self, 'apellido_materno', n.get_str_value()),
            "apellidoPaterno": lambda n : setattr(self, 'apellido_paterno', n.get_str_value()),
            "causaDeBaja": lambda n : setattr(self, 'causa_de_baja', n.get_str_value()),
            "claveDelTrabajador": lambda n : setattr(self, 'clave_del_trabajador', n.get_str_value()),
            "curp": lambda n : setattr(self, 'curp', n.get_str_value()),
            "fechaDeMovimiento": lambda n : setattr(self, 'fecha_de_movimiento', dateparser.parse(n.get_str_value())),
            "jornada": lambda n : setattr(self, 'jornada', n.get_str_value()),
            "nombre": lambda n : setattr(self, 'nombre', n.get_str_value()),
            "nss": lambda n : setattr(self, 'nss', n.get_str_value()),
            "registroPatronal": lambda n : setattr(self, 'registro_patronal', n.get_str_value()),
            "salarioDiarioIntegrado": lambda n : setattr(self, 'salario_diario_integrado', n.get_float_value()),
            "tipoDeMovimiento": lambda n : setattr(self, 'tipo_de_movimiento', n.get_str_value()),
            "tipoDeSalario": lambda n : setattr(self, 'tipo_de_salario', n.get_str_value()),
            "tipoDeTrabajador": lambda n : setattr(self, 'tipo_de_trabajador', n.get_str_value()),
            "umf": lambda n : setattr(self, 'umf', n.get_str_value()),
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
        writer.write_str_value("causaDeBaja", self.causa_de_baja)
        writer.write_str_value("claveDelTrabajador", self.clave_del_trabajador)
        writer.write_str_value("curp", self.curp)
        writer.write_date_value("fechaDeMovimiento", self.fecha_de_movimiento)
        writer.write_str_value("jornada", self.jornada)
        writer.write_str_value("nombre", self.nombre)
        writer.write_str_value("nss", self.nss)
        writer.write_str_value("registroPatronal", self.registro_patronal)
        writer.write_float_value("salarioDiarioIntegrado", self.salario_diario_integrado)
        writer.write_str_value("tipoDeMovimiento", self.tipo_de_movimiento)
        writer.write_str_value("tipoDeSalario", self.tipo_de_salario)
        writer.write_str_value("tipoDeTrabajador", self.tipo_de_trabajador)
        writer.write_str_value("umf", self.umf)
        writer.write_additional_data_value(self.additional_data)
    

