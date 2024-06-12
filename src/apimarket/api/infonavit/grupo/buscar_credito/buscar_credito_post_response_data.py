from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional

from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter


@dataclass
class BuscarCreditoPostResponse_data(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # Apellido materno del solicitante
    ap_materno: Optional[str] = None
    # Apellido paterno del solicitante
    ap_paterno: Optional[str] = None
    # Correo electrónico personal del solicitante
    email_personal: Optional[str] = None
    # Conjunto de estatus de INFONAVIT: nulo (no cuenta con crédito), AC (cuenta con crédito)
    estatus_credito: Optional[str] = None
    # Fecha de cierre del crédito en formato YYYYMMDD, puede estar vacío si el crédito está activo
    fecha_cierre: Optional[str] = None
    # Fecha de origen del crédito en formato YYYYMMDD
    fecha_origen: Optional[str] = None
    # Número total de meses en los que el derechohabiente no ha hecho su contribución
    mesesomisos: Optional[str] = None
    # Tipo de moneda en la que está denotado el crédito
    moneda: Optional[str] = None
    # Nombre del solicitante
    nombre: Optional[str] = None
    # Número de Seguro Social del solicitante
    nss: Optional[str] = None
    # Número del crédito asignado
    num_credito: Optional[str] = None
    # En el contexto de instituciones crediticias, es el identificador asignado al conjunto de préstamos hipotecarios que se agrupan para ser vendidos como un producto de inversión
    pool: Optional[str] = None
    # Tipo de crédito que ofrece el INFONAVIT, en tu caso, Hipotecaria Total (HiTo)
    producto: Optional[str] = None
    # Régimen de amortización que puede ser ROA (Régimen ordinario de Amortización) o REA (Régimen especial de Amortización)
    regimen: Optional[str] = None
    # Registro Federal de Contribuyentes del solicitante
    rfc: Optional[str] = None
    # CURP del solicitante
    scurp: Optional[str] = None
    # Situación actual del crédito
    situacioncredito: Optional[str] = None
    # Número de teléfono celular del solicitante
    telefono_celular: Optional[str] = None
    # El conjunto de modalidades que INFONAVIT maneja: Hipotecario (estándar), COFINAVIT, COFINAVIT INGRESOS ADICIONALES, INFONAVIT TOTAL, TU SEGUNDO CRÉDITO INFONAVIT
    tipo_credito: Optional[str] = None

    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> BuscarCreditoPostResponse_data:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: BuscarCreditoPostResponse_data
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return BuscarCreditoPostResponse_data()

    def get_field_deserializers(self, ) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        fields: Dict[str, Callable[[Any], None]] = {
            "apMaterno": lambda n: setattr(self, 'ap_materno', n.get_str_value()),
            "apPaterno": lambda n: setattr(self, 'ap_paterno', n.get_str_value()),
            "emailPersonal": lambda n: setattr(self, 'email_personal', n.get_str_value()),
            "estatus_credito": lambda n: setattr(self, 'estatus_credito', n.get_str_value()),
            "fechaCierre": lambda n: setattr(self, 'fecha_cierre', n.get_str_value()),
            "fechaOrigen": lambda n: setattr(self, 'fecha_origen', n.get_str_value()),
            "mesesomisos": lambda n: setattr(self, 'mesesomisos', n.get_str_value()),
            "moneda": lambda n: setattr(self, 'moneda', n.get_str_value()),
            "nombre": lambda n: setattr(self, 'nombre', n.get_str_value()),
            "nss": lambda n: setattr(self, 'nss', n.get_str_value()),
            "num_credito": lambda n: setattr(self, 'num_credito', n.get_str_value()),
            "pool": lambda n: setattr(self, 'pool', n.get_str_value()),
            "producto": lambda n: setattr(self, 'producto', n.get_str_value()),
            "regimen": lambda n: setattr(self, 'regimen', n.get_str_value()),
            "rfc": lambda n: setattr(self, 'rfc', n.get_str_value()),
            "scurp": lambda n: setattr(self, 'scurp', n.get_str_value()),
            "situacioncredito": lambda n: setattr(self, 'situacioncredito', n.get_str_value()),
            "telefonoCelular": lambda n: setattr(self, 'telefono_celular', n.get_str_value()),
            "tipo_credito": lambda n: setattr(self, 'tipo_credito', n.get_str_value()), }
        return fields

    def serialize(self, writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if not writer:
            raise TypeError("writer cannot be null.")
        writer.write_str_value("apMaterno", self.ap_materno)
        writer.write_str_value("apPaterno", self.ap_paterno)
        writer.write_str_value("emailPersonal", self.email_personal)
        writer.write_str_value("estatus_credito", self.estatus_credito)
        writer.write_str_value("fechaCierre", self.fecha_cierre)
        writer.write_str_value("fechaOrigen", self.fecha_origen)
        writer.write_str_value("mesesomisos", self.mesesomisos)
        writer.write_str_value("moneda", self.moneda)
        writer.write_str_value("nombre", self.nombre)
        writer.write_str_value("nss", self.nss)
        writer.write_str_value("num_credito", self.num_credito)
        writer.write_str_value("pool", self.pool)
        writer.write_str_value("producto", self.producto)
        writer.write_str_value("regimen", self.regimen)
        writer.write_str_value("rfc", self.rfc)
        writer.write_str_value("scurp", self.scurp)
        writer.write_str_value("situacioncredito", self.situacioncredito)
        writer.write_str_value("telefonoCelular", self.telefono_celular)
        writer.write_str_value("tipo_credito", self.tipo_credito)
        writer.write_additional_data_value(self.additional_data)
