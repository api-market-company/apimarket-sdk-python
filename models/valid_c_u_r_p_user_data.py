from __future__ import annotations
import datetime
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union
import dateparser

if TYPE_CHECKING:
    from .doc_probatorio_data import DocProbatorioData
    from .historial_data import HistorialData
    from .valid_c_u_r_p_user_data_sexo import ValidCURPUserData_sexo

@dataclass
class ValidCURPUserData(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The apellidoMaterno property
    apellido_materno: Optional[str] = None
    # The apellidoPaterno property
    apellido_paterno: Optional[str] = None
    # The curp property
    curp: Optional[str] = None
    # The datosDocProbatorio property
    datos_doc_probatorio: Optional[DocProbatorioData] = None
    # The docProbatorio property
    doc_probatorio: Optional[int] = None
    # The estadoNacimiento property
    estado_nacimiento: Optional[str] = None
    # The fechaNacimiento property
    fecha_nacimiento: Optional[datetime.date] = None
    # The historial property
    historial: Optional[HistorialData] = None
    # The nombres property
    nombres: Optional[str] = None
    # The paisNacimiento property
    pais_nacimiento: Optional[str] = None
    # The sexo property
    sexo: Optional[ValidCURPUserData_sexo] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ValidCURPUserData:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ValidCURPUserData
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return ValidCURPUserData()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .doc_probatorio_data import DocProbatorioData
        from .historial_data import HistorialData
        from .valid_c_u_r_p_user_data_sexo import ValidCURPUserData_sexo

        from .doc_probatorio_data import DocProbatorioData
        from .historial_data import HistorialData
        from .valid_c_u_r_p_user_data_sexo import ValidCURPUserData_sexo

        fields: Dict[str, Callable[[Any], None]] = {
            "apellidoMaterno": lambda n : setattr(self, 'apellido_materno', n.get_str_value()),
            "apellidoPaterno": lambda n : setattr(self, 'apellido_paterno', n.get_str_value()),
            "curp": lambda n : setattr(self, 'curp', n.get_str_value()),
            "datosDocProbatorio": lambda n : setattr(self, 'datos_doc_probatorio', n.get_object_value(DocProbatorioData)),
            "docProbatorio": lambda n : setattr(self, 'doc_probatorio', n.get_int_value()),
            "estadoNacimiento": lambda n : setattr(self, 'estado_nacimiento', n.get_str_value()),
            "fechaNacimiento": lambda n : setattr(self, 'fecha_nacimiento', dateparser.parse(n.get_str_value())),
            "historial": lambda n : setattr(self, 'historial', n.get_object_value(HistorialData)),
            "nombres": lambda n : setattr(self, 'nombres', n.get_str_value()),
            "paisNacimiento": lambda n : setattr(self, 'pais_nacimiento', n.get_str_value()),
            "sexo": lambda n : setattr(self, 'sexo', n.get_enum_value(ValidCURPUserData_sexo)),
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
        writer.write_object_value("datosDocProbatorio", self.datos_doc_probatorio)
        writer.write_int_value("docProbatorio", self.doc_probatorio)
        writer.write_str_value("estadoNacimiento", self.estado_nacimiento)
        writer.write_date_value("fechaNacimiento", self.fecha_nacimiento)
        writer.write_object_value("historial", self.historial)
        writer.write_str_value("nombres", self.nombres)
        writer.write_str_value("paisNacimiento", self.pais_nacimiento)
        writer.write_enum_value("sexo", self.sexo)
        writer.write_additional_data_value(self.additional_data)
    

