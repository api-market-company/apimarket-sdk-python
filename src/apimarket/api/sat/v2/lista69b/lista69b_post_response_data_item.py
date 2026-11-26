from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, Optional


@dataclass
class Lista69bPostResponseDataItem(AdditionalDataHolder, Parsable):
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # Campos base
    no: Optional[int] = None
    rfc: Optional[str] = None
    fuente: Optional[str] = None
    nombre_contribuyente: Optional[str] = None
    situacion_contribuyente: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    # Presunción SAT
    presuncion_sat_oficio: Optional[str] = None
    presuncion_sat_oficio_fecha: Optional[str] = None
    presuncion_sat_publicacion: Optional[str] = None

    # Presunción DOF
    presuncion_dof_oficio: Optional[str] = None
    presuncion_dof_oficio_fecha: Optional[str] = None
    presuncion_dof_publicacion: Optional[str] = None

    # Desvirtuados SAT
    desvirtuados_sat_oficio: Optional[str] = None
    desvirtuados_sat_oficio_fecha: Optional[str] = None
    desvirtuados_sat_publicacion: Optional[str] = None

    # Desvirtuados DOF
    desvirtuados_dof_oficio: Optional[str] = None
    desvirtuados_dof_oficio_fecha: Optional[str] = None
    desvirtuados_dof_publicacion: Optional[str] = None

    # Definitivos SAT
    definitivos_sat_oficio: Optional[str] = None
    definitivos_sat_oficio_fecha: Optional[str] = None
    definitivos_sat_publicacion: Optional[str] = None

    # Definitivos DOF
    definitivos_dof_oficio: Optional[str] = None
    definitivos_dof_oficio_fecha: Optional[str] = None
    definitivos_dof_publicacion: Optional[str] = None

    # Global definitivos SAT
    global_definitivos_sat_oficio: Optional[str] = None
    global_definitivos_sat_oficio_fecha: Optional[str] = None
    global_definitivos_sat_publicacion: Optional[str] = None

    # Global definitivos DOF
    global_definitivos_dof_oficio: Optional[str] = None
    global_definitivos_dof_oficio_fecha: Optional[str] = None
    global_definitivos_dof_publicacion: Optional[str] = None

    # Sentencia SAT
    sentencia_sat_oficio: Optional[str] = None
    sentencia_sat_oficio_fecha: Optional[str] = None
    sentencia_sat_publicacion: Optional[str] = None

    # Sentencia DOF
    sentencia_dof_oficio: Optional[str] = None
    sentencia_dof_oficio_fecha: Optional[str] = None
    sentencia_dof_publicacion: Optional[str] = None

    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Lista69bPostResponseDataItem:
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return Lista69bPostResponseDataItem()

    def get_field_deserializers(self) -> Dict[str, Callable[[ParseNode], None]]:
        return {
            "no":                                  lambda n: setattr(self, 'no', n.get_int_value()),
            "rfc":                                 lambda n: setattr(self, 'rfc', n.get_str_value()),
            "fuente":                              lambda n: setattr(self, 'fuente', n.get_str_value()),
            "nombre_contribuyente":                lambda n: setattr(self, 'nombre_contribuyente', n.get_str_value()),
            "situacion_contribuyente":             lambda n: setattr(self, 'situacion_contribuyente', n.get_str_value()),
            "created_at":                          lambda n: setattr(self, 'created_at', n.get_str_value()),
            "updated_at":                          lambda n: setattr(self, 'updated_at', n.get_str_value()),
            "presuncion_sat_oficio":               lambda n: setattr(self, 'presuncion_sat_oficio', n.get_str_value()),
            "presuncion_sat_oficio_fecha":         lambda n: setattr(self, 'presuncion_sat_oficio_fecha', n.get_str_value()),
            "presuncion_sat_publicacion":          lambda n: setattr(self, 'presuncion_sat_publicacion', n.get_str_value()),
            "presuncion_dof_oficio":               lambda n: setattr(self, 'presuncion_dof_oficio', n.get_str_value()),
            "presuncion_dof_oficio_fecha":         lambda n: setattr(self, 'presuncion_dof_oficio_fecha', n.get_str_value()),
            "presuncion_dof_publicacion":          lambda n: setattr(self, 'presuncion_dof_publicacion', n.get_str_value()),
            "desvirtuados_sat_oficio":             lambda n: setattr(self, 'desvirtuados_sat_oficio', n.get_str_value()),
            "desvirtuados_sat_oficio_fecha":       lambda n: setattr(self, 'desvirtuados_sat_oficio_fecha', n.get_str_value()),
            "desvirtuados_sat_publicacion":        lambda n: setattr(self, 'desvirtuados_sat_publicacion', n.get_str_value()),
            "desvirtuados_dof_oficio":             lambda n: setattr(self, 'desvirtuados_dof_oficio', n.get_str_value()),
            "desvirtuados_dof_oficio_fecha":       lambda n: setattr(self, 'desvirtuados_dof_oficio_fecha', n.get_str_value()),
            "desvirtuados_dof_publicacion":        lambda n: setattr(self, 'desvirtuados_dof_publicacion', n.get_str_value()),
            "definitivos_sat_oficio":              lambda n: setattr(self, 'definitivos_sat_oficio', n.get_str_value()),
            "definitivos_sat_oficio_fecha":        lambda n: setattr(self, 'definitivos_sat_oficio_fecha', n.get_str_value()),
            "definitivos_sat_publicacion":         lambda n: setattr(self, 'definitivos_sat_publicacion', n.get_str_value()),
            "definitivos_dof_oficio":              lambda n: setattr(self, 'definitivos_dof_oficio', n.get_str_value()),
            "definitivos_dof_oficio_fecha":        lambda n: setattr(self, 'definitivos_dof_oficio_fecha', n.get_str_value()),
            "definitivos_dof_publicacion":         lambda n: setattr(self, 'definitivos_dof_publicacion', n.get_str_value()),
            "global_definitivos_sat_oficio":       lambda n: setattr(self, 'global_definitivos_sat_oficio', n.get_str_value()),
            "global_definitivos_sat_oficio_fecha": lambda n: setattr(self, 'global_definitivos_sat_oficio_fecha', n.get_str_value()),
            "global_definitivos_sat_publicacion":  lambda n: setattr(self, 'global_definitivos_sat_publicacion', n.get_str_value()),
            "global_definitivos_dof_oficio":       lambda n: setattr(self, 'global_definitivos_dof_oficio', n.get_str_value()),
            "global_definitivos_dof_oficio_fecha": lambda n: setattr(self, 'global_definitivos_dof_oficio_fecha', n.get_str_value()),
            "global_definitivos_dof_publicacion":  lambda n: setattr(self, 'global_definitivos_dof_publicacion', n.get_str_value()),
            "sentencia_sat_oficio":                lambda n: setattr(self, 'sentencia_sat_oficio', n.get_str_value()),
            "sentencia_sat_oficio_fecha":          lambda n: setattr(self, 'sentencia_sat_oficio_fecha', n.get_str_value()),
            "sentencia_sat_publicacion":           lambda n: setattr(self, 'sentencia_sat_publicacion', n.get_str_value()),
            "sentencia_dof_oficio":                lambda n: setattr(self, 'sentencia_dof_oficio', n.get_str_value()),
            "sentencia_dof_oficio_fecha":          lambda n: setattr(self, 'sentencia_dof_oficio_fecha', n.get_str_value()),
            "sentencia_dof_publicacion":           lambda n: setattr(self, 'sentencia_dof_publicacion', n.get_str_value()),
        }

    def serialize(self, writer: SerializationWriter) -> None:
        if not writer:
            raise TypeError("writer cannot be null.")
        writer.write_int_value("no", self.no)
        writer.write_str_value("rfc", self.rfc)
        writer.write_str_value("fuente", self.fuente)
        writer.write_str_value("nombre_contribuyente", self.nombre_contribuyente)
        writer.write_str_value("situacion_contribuyente", self.situacion_contribuyente)
        writer.write_str_value("created_at", self.created_at)
        writer.write_str_value("updated_at", self.updated_at)
        writer.write_str_value("presuncion_sat_oficio", self.presuncion_sat_oficio)
        writer.write_str_value("presuncion_sat_oficio_fecha", self.presuncion_sat_oficio_fecha)
        writer.write_str_value("presuncion_sat_publicacion", self.presuncion_sat_publicacion)
        writer.write_str_value("presuncion_dof_oficio", self.presuncion_dof_oficio)
        writer.write_str_value("presuncion_dof_oficio_fecha", self.presuncion_dof_oficio_fecha)
        writer.write_str_value("presuncion_dof_publicacion", self.presuncion_dof_publicacion)
        writer.write_str_value("desvirtuados_sat_oficio", self.desvirtuados_sat_oficio)
        writer.write_str_value("desvirtuados_sat_oficio_fecha", self.desvirtuados_sat_oficio_fecha)
        writer.write_str_value("desvirtuados_sat_publicacion", self.desvirtuados_sat_publicacion)
        writer.write_str_value("desvirtuados_dof_oficio", self.desvirtuados_dof_oficio)
        writer.write_str_value("desvirtuados_dof_oficio_fecha", self.desvirtuados_dof_oficio_fecha)
        writer.write_str_value("desvirtuados_dof_publicacion", self.desvirtuados_dof_publicacion)
        writer.write_str_value("definitivos_sat_oficio", self.definitivos_sat_oficio)
        writer.write_str_value("definitivos_sat_oficio_fecha", self.definitivos_sat_oficio_fecha)
        writer.write_str_value("definitivos_sat_publicacion", self.definitivos_sat_publicacion)
        writer.write_str_value("definitivos_dof_oficio", self.definitivos_dof_oficio)
        writer.write_str_value("definitivos_dof_oficio_fecha", self.definitivos_dof_oficio_fecha)
        writer.write_str_value("definitivos_dof_publicacion", self.definitivos_dof_publicacion)
        writer.write_str_value("global_definitivos_sat_oficio", self.global_definitivos_sat_oficio)
        writer.write_str_value("global_definitivos_sat_oficio_fecha", self.global_definitivos_sat_oficio_fecha)
        writer.write_str_value("global_definitivos_sat_publicacion", self.global_definitivos_sat_publicacion)
        writer.write_str_value("global_definitivos_dof_oficio", self.global_definitivos_dof_oficio)
        writer.write_str_value("global_definitivos_dof_oficio_fecha", self.global_definitivos_dof_oficio_fecha)
        writer.write_str_value("global_definitivos_dof_publicacion", self.global_definitivos_dof_publicacion)
        writer.write_str_value("sentencia_sat_oficio", self.sentencia_sat_oficio)
        writer.write_str_value("sentencia_sat_oficio_fecha", self.sentencia_sat_oficio_fecha)
        writer.write_str_value("sentencia_sat_publicacion", self.sentencia_sat_publicacion)
        writer.write_str_value("sentencia_dof_oficio", self.sentencia_dof_oficio)
        writer.write_str_value("sentencia_dof_oficio_fecha", self.sentencia_dof_oficio_fecha)
        writer.write_str_value("sentencia_dof_publicacion", self.sentencia_dof_publicacion)
        writer.write_additional_data_value(self.additional_data)
