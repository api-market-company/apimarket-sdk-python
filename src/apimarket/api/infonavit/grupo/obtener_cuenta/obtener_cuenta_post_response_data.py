from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

@dataclass
class ObtenerCuentaPostResponse_data(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # Aportación del solicitante
    aportacion: Optional[str] = None
    # Bimestre correspondiente
    bimestre: Optional[str] = None
    # Fecha de pago, puede estar vacío si no hay fecha de pago
    fecha_pago: Optional[str] = None
    # Número de Seguro Social del solicitante
    n_s_s: Optional[int] = None
    # Nombre de la empresa, puede estar vacío si no hay empresa registrada
    nombre_empresa: Optional[str] = None
    # Saldo anterior del SAR. Se refiere al saldo que existía en la cuenta del trabajador en un período anterior específico. Este saldo no incluye las nuevas aportaciones ni los rendimientos generados desde la última vez que se actualizó el saldo.
    saldo_anterior: Optional[str] = None
    # Saldo total del SAR. Es la suma de todas las aportaciones realizadas a la cuenta individual del trabajador, incluyendo las del SAR 92 y SAR 97, junto con los rendimientos generados. Representa el monto total disponible en la cuenta de ahorro para el retiro del trabajador.
    saldo_s_a_r_total: Optional[float] = None
    # Saldo del SAR del año 92. Se refiere a las aportaciones realizadas al Sistema de Ahorro para el Retiro antes de la reforma de 1997.
    saldo_s_a_r92: Optional[str] = None
    # Saldo del SAR del año 97. Se refiere a las aportaciones realizadas después de la reforma de 1997.
    saldo_s_a_r97: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ObtenerCuentaPostResponse_data:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ObtenerCuentaPostResponse_data
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return ObtenerCuentaPostResponse_data()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        fields: Dict[str, Callable[[Any], None]] = {
            "aportacion": lambda n : setattr(self, 'aportacion', n.get_str_value()),
            "bimestre": lambda n : setattr(self, 'bimestre', n.get_str_value()),
            "fechaPago": lambda n : setattr(self, 'fecha_pago', n.get_str_value()),
            "NSS": lambda n : setattr(self, 'n_s_s', n.get_int_value()),
            "nombreEmpresa": lambda n : setattr(self, 'nombre_empresa', n.get_str_value()),
            "saldoAnterior": lambda n : setattr(self, 'saldo_anterior', n.get_str_value()),
            "saldoSARTotal": lambda n : setattr(self, 'saldo_s_a_r_total', n.get_float_value()),
            "saldoSAR92": lambda n : setattr(self, 'saldo_s_a_r92', n.get_str_value()),
            "saldoSAR97": lambda n : setattr(self, 'saldo_s_a_r97', n.get_str_value()),
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
        writer.write_str_value("aportacion", self.aportacion)
        writer.write_str_value("bimestre", self.bimestre)
        writer.write_str_value("fechaPago", self.fecha_pago)
        writer.write_int_value("NSS", self.n_s_s)
        writer.write_str_value("nombreEmpresa", self.nombre_empresa)
        writer.write_str_value("saldoAnterior", self.saldo_anterior)
        writer.write_float_value("saldoSARTotal", self.saldo_s_a_r_total)
        writer.write_str_value("saldoSAR92", self.saldo_s_a_r92)
        writer.write_str_value("saldoSAR97", self.saldo_s_a_r97)
        writer.write_additional_data_value(self.additional_data)
    

