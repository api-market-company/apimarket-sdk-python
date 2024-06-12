from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .obtener_datos_post_response_actividades import ObtenerDatosPostResponse_actividades
    from .obtener_datos_post_response_codigos_postales import ObtenerDatosPostResponse_codigosPostales
    from .obtener_datos_post_response_obligaciones import ObtenerDatosPostResponse_obligaciones
    from .obtener_datos_post_response_regimenes import ObtenerDatosPostResponse_regimenes

@dataclass
class ObtenerDatosPostResponse(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The actividades property
    actividades: Optional[List[ObtenerDatosPostResponse_actividades]] = None
    # The codigosPostales property
    codigos_postales: Optional[List[ObtenerDatosPostResponse_codigosPostales]] = None
    # The correoElectronico property
    correo_electronico: Optional[str] = None
    # The nombreCompleto property
    nombre_completo: Optional[str] = None
    # The obligaciones property
    obligaciones: Optional[List[ObtenerDatosPostResponse_obligaciones]] = None
    # The puedeFacturar property
    puede_facturar: Optional[bool] = None
    # The regimenes property
    regimenes: Optional[List[ObtenerDatosPostResponse_regimenes]] = None
    # The rfc property
    rfc: Optional[str] = None
    # The tipoPersona property
    tipo_persona: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ObtenerDatosPostResponse:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ObtenerDatosPostResponse
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return ObtenerDatosPostResponse()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .obtener_datos_post_response_actividades import ObtenerDatosPostResponse_actividades
        from .obtener_datos_post_response_codigos_postales import ObtenerDatosPostResponse_codigosPostales
        from .obtener_datos_post_response_obligaciones import ObtenerDatosPostResponse_obligaciones
        from .obtener_datos_post_response_regimenes import ObtenerDatosPostResponse_regimenes

        from .obtener_datos_post_response_actividades import ObtenerDatosPostResponse_actividades
        from .obtener_datos_post_response_codigos_postales import ObtenerDatosPostResponse_codigosPostales
        from .obtener_datos_post_response_obligaciones import ObtenerDatosPostResponse_obligaciones
        from .obtener_datos_post_response_regimenes import ObtenerDatosPostResponse_regimenes

        fields: Dict[str, Callable[[Any], None]] = {
            "actividades": lambda n : setattr(self, 'actividades', n.get_collection_of_object_values(ObtenerDatosPostResponse_actividades)),
            "codigosPostales": lambda n : setattr(self, 'codigos_postales', n.get_collection_of_object_values(ObtenerDatosPostResponse_codigosPostales)),
            "correoElectronico": lambda n : setattr(self, 'correo_electronico', n.get_str_value()),
            "nombreCompleto": lambda n : setattr(self, 'nombre_completo', n.get_str_value()),
            "obligaciones": lambda n : setattr(self, 'obligaciones', n.get_collection_of_object_values(ObtenerDatosPostResponse_obligaciones)),
            "puedeFacturar": lambda n : setattr(self, 'puede_facturar', n.get_bool_value()),
            "regimenes": lambda n : setattr(self, 'regimenes', n.get_collection_of_object_values(ObtenerDatosPostResponse_regimenes)),
            "rfc": lambda n : setattr(self, 'rfc', n.get_str_value()),
            "tipoPersona": lambda n : setattr(self, 'tipo_persona', n.get_str_value()),
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
        writer.write_collection_of_object_values("actividades", self.actividades)
        writer.write_collection_of_object_values("codigosPostales", self.codigos_postales)
        writer.write_str_value("correoElectronico", self.correo_electronico)
        writer.write_str_value("nombreCompleto", self.nombre_completo)
        writer.write_collection_of_object_values("obligaciones", self.obligaciones)
        writer.write_bool_value("puedeFacturar", self.puede_facturar)
        writer.write_collection_of_object_values("regimenes", self.regimenes)
        writer.write_str_value("rfc", self.rfc)
        writer.write_str_value("tipoPersona", self.tipo_persona)
        writer.write_additional_data_value(self.additional_data)
    

