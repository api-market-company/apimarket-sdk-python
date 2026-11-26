from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

@dataclass
class ValidarCertificadoGetResponseData(AdditionalDataHolder, Parsable):
    additional_data: Dict[str, Any] = field(default_factory=dict)
    certificado_id: Optional[int] = None
    folio: Optional[str] = None
    nombres: Optional[str] = None
    primer_apellido: Optional[str] = None
    segundo_apellido: Optional[str] = None
    institucion: Optional[str] = None
    fecha_certificado: Optional[str] = None
    estatus: Optional[str] = None
    tipo_certificacion: Optional[str] = None
    tipo_certificado: Optional[str] = None
    promedio: Optional[str] = None
    carrera: Optional[str] = None
    tipo: Optional[str] = None
    id_entidad_federativa: Optional[str] = None
    entidad_federativa: Optional[str] = None
    fecha_emision: Optional[str] = None

    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ValidarCertificadoGetResponseData:
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return ValidarCertificadoGetResponseData()

    def get_field_deserializers(self) -> Dict[str, Callable[[ParseNode], None]]:
        return {
            "certificadoId":       lambda n: setattr(self, 'certificado_id', n.get_int_value()),
            "folio":               lambda n: setattr(self, 'folio', n.get_str_value()),
            "nombres":             lambda n: setattr(self, 'nombres', n.get_str_value()),
            "primerApellido":      lambda n: setattr(self, 'primer_apellido', n.get_str_value()),
            "segundoApellido":     lambda n: setattr(self, 'segundo_apellido', n.get_str_value()),
            "institucion":         lambda n: setattr(self, 'institucion', n.get_str_value()),
            "fechaCertificado":    lambda n: setattr(self, 'fecha_certificado', n.get_str_value()),
            "estatus":             lambda n: setattr(self, 'estatus', n.get_str_value()),
            "tipoCertificacion":   lambda n: setattr(self, 'tipo_certificacion', n.get_str_value()),
            "tipoCertificado":     lambda n: setattr(self, 'tipo_certificado', n.get_str_value()),
            "promedio":            lambda n: setattr(self, 'promedio', n.get_str_value()),
            "carrera":             lambda n: setattr(self, 'carrera', n.get_str_value()),
            "tipo":                lambda n: setattr(self, 'tipo', n.get_str_value()),
            "idEntidadFederativa": lambda n: setattr(self, 'id_entidad_federativa', n.get_str_value()),
            "entidadFederativa":   lambda n: setattr(self, 'entidad_federativa', n.get_str_value()),
            "fechaEmision":        lambda n: setattr(self, 'fecha_emision', n.get_str_value()),
        }

    def serialize(self, writer: SerializationWriter) -> None:
        if not writer:
            raise TypeError("writer cannot be null.")
        writer.write_int_value("certificadoId", self.certificado_id)
        writer.write_str_value("folio", self.folio)
        writer.write_str_value("nombres", self.nombres)
        writer.write_str_value("primerApellido", self.primer_apellido)
        writer.write_str_value("segundoApellido", self.segundo_apellido)
        writer.write_str_value("institucion", self.institucion)
        writer.write_str_value("fechaCertificado", self.fecha_certificado)
        writer.write_str_value("estatus", self.estatus)
        writer.write_str_value("tipoCertificacion", self.tipo_certificacion)
        writer.write_str_value("tipoCertificado", self.tipo_certificado)
        writer.write_str_value("promedio", self.promedio)
        writer.write_str_value("carrera", self.carrera)
        writer.write_str_value("tipo", self.tipo)
        writer.write_str_value("idEntidadFederativa", self.id_entidad_federativa)
        writer.write_str_value("entidadFederativa", self.entidad_federativa)
        writer.write_str_value("fechaEmision", self.fecha_emision)
        writer.write_additional_data_value(self.additional_data)
