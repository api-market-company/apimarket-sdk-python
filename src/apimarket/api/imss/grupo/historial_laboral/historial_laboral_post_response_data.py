from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .historial_laboral_post_response_data_historial_laboral import HistorialLaboralPostResponse_data_historialLaboral
    from .historial_laboral_post_response_data_semanas_cotizadas import HistorialLaboralPostResponse_data_semanasCotizadas

@dataclass
class HistorialLaboralPostResponse_data(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The cadenaOriginal property
    cadena_original: Optional[str] = None
    # URL firmada de la constancia en PDF. Puede ser descargada o visualizada en el navegador por un periodo de 2 horas.
    constancia: Optional[str] = None
    # The curp property
    curp: Optional[str] = None
    # The historialLaboral property
    historial_laboral: Optional[List[HistorialLaboralPostResponse_data_historialLaboral]] = None
    # The nombre property
    nombre: Optional[str] = None
    # The nss property
    nss: Optional[str] = None
    # The numeroDeSerie property
    numero_de_serie: Optional[str] = None
    # The secuenciaNotarial property
    secuencia_notarial: Optional[str] = None
    # The selloDigital property
    sello_digital: Optional[str] = None
    # The semanasCotizadas property
    semanas_cotizadas: Optional[HistorialLaboralPostResponse_data_semanasCotizadas] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> HistorialLaboralPostResponse_data:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: HistorialLaboralPostResponse_data
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return HistorialLaboralPostResponse_data()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .historial_laboral_post_response_data_historial_laboral import HistorialLaboralPostResponse_data_historialLaboral
        from .historial_laboral_post_response_data_semanas_cotizadas import HistorialLaboralPostResponse_data_semanasCotizadas

        from .historial_laboral_post_response_data_historial_laboral import HistorialLaboralPostResponse_data_historialLaboral
        from .historial_laboral_post_response_data_semanas_cotizadas import HistorialLaboralPostResponse_data_semanasCotizadas

        fields: Dict[str, Callable[[Any], None]] = {
            "cadenaOriginal": lambda n : setattr(self, 'cadena_original', n.get_str_value()),
            "constancia": lambda n : setattr(self, 'constancia', n.get_str_value()),
            "curp": lambda n : setattr(self, 'curp', n.get_str_value()),
            "historialLaboral": lambda n : setattr(self, 'historial_laboral', n.get_collection_of_object_values(HistorialLaboralPostResponse_data_historialLaboral)),
            "nombre": lambda n : setattr(self, 'nombre', n.get_str_value()),
            "nss": lambda n : setattr(self, 'nss', n.get_str_value()),
            "numeroDeSerie": lambda n : setattr(self, 'numero_de_serie', n.get_str_value()),
            "secuenciaNotarial": lambda n : setattr(self, 'secuencia_notarial', n.get_str_value()),
            "selloDigital": lambda n : setattr(self, 'sello_digital', n.get_str_value()),
            "semanasCotizadas": lambda n : setattr(self, 'semanas_cotizadas', n.get_object_value(HistorialLaboralPostResponse_data_semanasCotizadas)),
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
        writer.write_str_value("cadenaOriginal", self.cadena_original)
        writer.write_str_value("constancia", self.constancia)
        writer.write_str_value("curp", self.curp)
        writer.write_collection_of_object_values("historialLaboral", self.historial_laboral)
        writer.write_str_value("nombre", self.nombre)
        writer.write_str_value("nss", self.nss)
        writer.write_str_value("numeroDeSerie", self.numero_de_serie)
        writer.write_str_value("secuenciaNotarial", self.secuencia_notarial)
        writer.write_str_value("selloDigital", self.sello_digital)
        writer.write_object_value("semanasCotizadas", self.semanas_cotizadas)
        writer.write_additional_data_value(self.additional_data)
    

