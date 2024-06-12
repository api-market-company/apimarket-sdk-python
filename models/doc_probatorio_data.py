from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

@dataclass
class DocProbatorioData(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The anioReg property
    anio_reg: Optional[int] = None
    # The claveEntidadRegistro property
    clave_entidad_registro: Optional[str] = None
    # The claveMunicipioRegistro property
    clave_municipio_registro: Optional[int] = None
    # The entidadRegistro property
    entidad_registro: Optional[str] = None
    # The foja property
    foja: Optional[int] = None
    # The libro property
    libro: Optional[int] = None
    # The municipioRegistro property
    municipio_registro: Optional[str] = None
    # The numActa property
    num_acta: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> DocProbatorioData:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DocProbatorioData
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return DocProbatorioData()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        fields: Dict[str, Callable[[Any], None]] = {
            "anioReg": lambda n : setattr(self, 'anio_reg', n.get_int_value()),
            "claveEntidadRegistro": lambda n : setattr(self, 'clave_entidad_registro', n.get_str_value()),
            "claveMunicipioRegistro": lambda n : setattr(self, 'clave_municipio_registro', n.get_int_value()),
            "entidadRegistro": lambda n : setattr(self, 'entidad_registro', n.get_str_value()),
            "foja": lambda n : setattr(self, 'foja', n.get_int_value()),
            "libro": lambda n : setattr(self, 'libro', n.get_int_value()),
            "municipioRegistro": lambda n : setattr(self, 'municipio_registro', n.get_str_value()),
            "numActa": lambda n : setattr(self, 'num_acta', n.get_int_value()),
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
        writer.write_int_value("anioReg", self.anio_reg)
        writer.write_str_value("claveEntidadRegistro", self.clave_entidad_registro)
        writer.write_int_value("claveMunicipioRegistro", self.clave_municipio_registro)
        writer.write_str_value("entidadRegistro", self.entidad_registro)
        writer.write_int_value("foja", self.foja)
        writer.write_int_value("libro", self.libro)
        writer.write_str_value("municipioRegistro", self.municipio_registro)
        writer.write_int_value("numActa", self.num_acta)
        writer.write_additional_data_value(self.additional_data)
    

