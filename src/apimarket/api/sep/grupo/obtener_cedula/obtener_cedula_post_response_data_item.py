from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, Optional


@dataclass
class ObtenerCedulaPostResponseDataItem(AdditionalDataHolder, Parsable):
    additional_data: Dict[str, Any] = field(default_factory=dict)
    anioreg: Optional[int] = None
    fecha_titulacion: Optional[str] = None
    car_area: Optional[int] = None
    car_cons: Optional[int] = None
    car_nivel: Optional[int] = None
    car_sarea: Optional[int] = None
    curp: Optional[str] = None
    desins: Optional[str] = None
    foja: Optional[int] = None
    id_cedula: Optional[str] = None
    inscons: Optional[int] = None
    insedo: Optional[int] = None
    libro: Optional[int] = None
    materno: Optional[str] = None
    materno_m: Optional[str] = None
    nombre: Optional[str] = None
    nombre_m: Optional[str] = None
    numero: Optional[int] = None
    paterno: Optional[str] = None
    paterno_m: Optional[str] = None
    sexo: Optional[str] = None
    tipo: Optional[str] = None
    titulo: Optional[str] = None
    fecha_expedicion: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    entidad_nacimiento: Optional[str] = None
    sostenimiento: Optional[int] = None
    carrera: Optional[str] = None

    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ObtenerCedulaPostResponseDataItem:
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return ObtenerCedulaPostResponseDataItem()

    def get_field_deserializers(self) -> Dict[str, Callable[[ParseNode], None]]:
        return {
            "anioreg":           lambda n: setattr(self, 'anioreg', n.get_int_value()),
            "fechaTitulacion":   lambda n: setattr(self, 'fecha_titulacion', n.get_str_value()),
            "carArea":           lambda n: setattr(self, 'car_area', n.get_int_value()),
            "carCons":           lambda n: setattr(self, 'car_cons', n.get_int_value()),
            "carNivel":          lambda n: setattr(self, 'car_nivel', n.get_int_value()),
            "carSarea":          lambda n: setattr(self, 'car_sarea', n.get_int_value()),
            "curp":              lambda n: setattr(self, 'curp', n.get_str_value()),
            "desins":            lambda n: setattr(self, 'desins', n.get_str_value()),
            "foja":              lambda n: setattr(self, 'foja', n.get_int_value()),
            "idCedula":          lambda n: setattr(self, 'id_cedula', n.get_str_value()),
            "inscons":           lambda n: setattr(self, 'inscons', n.get_int_value()),
            "insedo":            lambda n: setattr(self, 'insedo', n.get_int_value()),
            "libro":             lambda n: setattr(self, 'libro', n.get_int_value()),
            "materno":           lambda n: setattr(self, 'materno', n.get_str_value()),
            "maternoM":          lambda n: setattr(self, 'materno_m', n.get_str_value()),
            "nombre":            lambda n: setattr(self, 'nombre', n.get_str_value()),
            "nombreM":           lambda n: setattr(self, 'nombre_m', n.get_str_value()),
            "numero":            lambda n: setattr(self, 'numero', n.get_int_value()),
            "paterno":           lambda n: setattr(self, 'paterno', n.get_str_value()),
            "paternoM":          lambda n: setattr(self, 'paterno_m', n.get_str_value()),
            "sexo":              lambda n: setattr(self, 'sexo', n.get_str_value()),
            "tipo":              lambda n: setattr(self, 'tipo', n.get_str_value()),
            "titulo":            lambda n: setattr(self, 'titulo', n.get_str_value()),
            "fechaExpedicion":   lambda n: setattr(self, 'fecha_expedicion', n.get_str_value()),
            "fechaNacimiento":   lambda n: setattr(self, 'fecha_nacimiento', n.get_str_value()),
            "entidadNacimiento": lambda n: setattr(self, 'entidad_nacimiento', n.get_str_value()),
            "sostenimiento":     lambda n: setattr(self, 'sostenimiento', n.get_int_value()),
            "carrera":           lambda n: setattr(self, 'carrera', n.get_str_value()),
        }

    def serialize(self, writer: SerializationWriter) -> None:
        if not writer:
            raise TypeError("writer cannot be null.")
        writer.write_int_value("anioreg", self.anioreg)
        writer.write_str_value("fechaTitulacion", self.fecha_titulacion)
        writer.write_int_value("carArea", self.car_area)
        writer.write_int_value("carCons", self.car_cons)
        writer.write_int_value("carNivel", self.car_nivel)
        writer.write_int_value("carSarea", self.car_sarea)
        writer.write_str_value("curp", self.curp)
        writer.write_str_value("desins", self.desins)
        writer.write_int_value("foja", self.foja)
        writer.write_str_value("idCedula", self.id_cedula)
        writer.write_int_value("inscons", self.inscons)
        writer.write_int_value("insedo", self.insedo)
        writer.write_int_value("libro", self.libro)
        writer.write_str_value("materno", self.materno)
        writer.write_str_value("maternoM", self.materno_m)
        writer.write_str_value("nombre", self.nombre)
        writer.write_str_value("nombreM", self.nombre_m)
        writer.write_int_value("numero", self.numero)
        writer.write_str_value("paterno", self.paterno)
        writer.write_str_value("paternoM", self.paterno_m)
        writer.write_str_value("sexo", self.sexo)
        writer.write_str_value("tipo", self.tipo)
        writer.write_str_value("titulo", self.titulo)
        writer.write_str_value("fechaExpedicion", self.fecha_expedicion)
        writer.write_str_value("fechaNacimiento", self.fecha_nacimiento)
        writer.write_str_value("entidadNacimiento", self.entidad_nacimiento)
        writer.write_int_value("sostenimiento", self.sostenimiento)
        writer.write_str_value("carrera", self.carrera)
        writer.write_additional_data_value(self.additional_data)
