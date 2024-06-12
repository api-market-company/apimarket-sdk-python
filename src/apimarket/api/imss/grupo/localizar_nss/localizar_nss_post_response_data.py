from __future__ import annotations
import datetime
from dataclasses import dataclass, field

import dateparser
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

@dataclass
class LocalizarNssPostResponse_data(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # Datos adicionales, puede estar vacío
    arco: Optional[str] = None
    # Clave Única de Registro de Población del solicitante
    cve_curp: Optional[str] = None
    # Correo electrónico del solicitante
    des_email: Optional[str] = None
    # Fecha de alta del solicitante en formato YYYY-MM-DD
    fec_alta: Optional[datetime.date] = None
    # Fecha de baja del solicitante en formato YYYY-MM-DD, puede estar vacío si no hay fecha de baja
    fec_baja: Optional[datetime.date] = None
    # Fecha de nacimiento del solicitante en formato YYYY-MM-DD
    fec_nacimiento: Optional[datetime.date] = None
    # Nombre del solicitante
    nom_nombre: Optional[str] = None
    # Número de Seguro Social del solicitante
    num_nss: Optional[str] = None
    # Apellido materno del solicitante
    ref_apellido_materno: Optional[str] = None
    # Apellido paterno del solicitante
    ref_apellido_paterno: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> LocalizarNssPostResponse_data:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: LocalizarNssPostResponse_data
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return LocalizarNssPostResponse_data()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        fields: Dict[str, Callable[[Any], None]] = {
            "arco": lambda n : setattr(self, 'arco', n.get_str_value()),
            "cveCurp": lambda n : setattr(self, 'cve_curp', n.get_str_value()),
            "desEmail": lambda n : setattr(self, 'des_email', n.get_str_value()),
            "fecAlta": lambda n : setattr(self, 'fec_alta', dateparser.parse(n.get_str_value())),
            "fecBaja": lambda n : setattr(self, 'fec_baja', dateparser.parse(n.get_str_value())),
            "fecNacimiento": lambda n : setattr(self, 'fec_nacimiento', dateparser.parse(n.get_str_value())),
            "nomNombre": lambda n : setattr(self, 'nom_nombre', n.get_str_value()),
            "numNss": lambda n : setattr(self, 'num_nss', n.get_str_value()),
            "refApellidoMaterno": lambda n : setattr(self, 'ref_apellido_materno', n.get_str_value()),
            "refApellidoPaterno": lambda n : setattr(self, 'ref_apellido_paterno', n.get_str_value()),
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
        writer.write_str_value("arco", self.arco)
        writer.write_str_value("cveCurp", self.cve_curp)
        writer.write_str_value("desEmail", self.des_email)
        writer.write_date_value("fecAlta", self.fec_alta)
        writer.write_date_value("fecBaja", self.fec_baja)
        writer.write_date_value("fecNacimiento", self.fec_nacimiento)
        writer.write_str_value("nomNombre", self.nom_nombre)
        writer.write_str_value("numNss", self.num_nss)
        writer.write_str_value("refApellidoMaterno", self.ref_apellido_materno)
        writer.write_str_value("refApellidoPaterno", self.ref_apellido_paterno)
        writer.write_additional_data_value(self.additional_data)
    

