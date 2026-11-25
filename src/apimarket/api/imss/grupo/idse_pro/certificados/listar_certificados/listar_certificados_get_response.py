from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, Optional


@dataclass
class Certificado(AdditionalDataHolder, Parsable):
    additional_data: Dict[str, Any] = field(default_factory=dict)

    id: Optional[str] = None
    name: Optional[str] = None
    custom_name: Optional[str] = None
    legal_name: Optional[str] = None
    rfc: Optional[str] = None
    serial: Optional[str] = None
    serial_number: Optional[str] = None
    version: Optional[int] = None
    mime: Optional[str] = None
    ocsp_status: Optional[str] = None
    user: Optional[str] = None
    organization_id: Optional[str] = None
    parent_certificate_id: Optional[str] = None
    issuer: Optional[str] = None
    issuer_common_name: Optional[str] = None
    issuer_organization: Optional[str] = None
    issuer_organization_unit: Optional[str] = None
    issuer_locality_name: Optional[str] = None
    issuer_state_or_province_name: Optional[str] = None
    issuer_country_name: Optional[str] = None
    issuer_postal_code: Optional[str] = None
    issuer_street_address: Optional[str] = None
    issuer_title: Optional[str] = None
    issuer_email_address: Optional[str] = None
    issuer_unique_identifier: Optional[str] = None
    subject_common_name: Optional[str] = None
    subject_organization: Optional[str] = None
    subject_organizational_unit_name: Optional[str] = None
    subject_email_address: Optional[str] = None
    subject_unique_identifier: Optional[str] = None
    subject_locality_name: Optional[str] = None
    subject_state_or_province_name: Optional[str] = None
    subject_country_name: Optional[str] = None
    subject_postal_code: Optional[str] = None
    subject_street_address: Optional[str] = None
    subject_title: Optional[str] = None
    subject_phone_number: Optional[str] = None
    subject_business_category: Optional[str] = None
    subject: Optional[str] = None
    valid_from: Optional[str] = None
    valid_until: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    subscription_expired_at: Optional[str] = None
    subscription_renewed_at: Optional[str] = None
    deactivated_at: Optional[str] = None
    deleted_at: Optional[str] = None
    can_sync_history: Optional[bool] = None
    can_associate_certificates: Optional[bool] = None
    total_prepaid_movements: Optional[int] = None
    rest_prepaid_movements: Optional[int] = None
    total_subscription_movements: Optional[int] = None
    rest_subscription_movements: Optional[int] = None

    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Certificado:
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return Certificado()

    def get_field_deserializers(self) -> Dict[str, Callable[[ParseNode], None]]:
        return {
            "id": lambda n: setattr(self, 'id', n.get_str_value()),
            "name": lambda n: setattr(self, 'name', n.get_str_value()),
            "custom_name": lambda n: setattr(self, 'custom_name', n.get_str_value()),
            "legal_name": lambda n: setattr(self, 'legal_name', n.get_str_value()),
            "rfc": lambda n: setattr(self, 'rfc', n.get_str_value()),
            "serial": lambda n: setattr(self, 'serial', n.get_str_value()),
            "serial_number": lambda n: setattr(self, 'serial_number', n.get_str_value()),
            "version": lambda n: setattr(self, 'version', n.get_int_value()),
            "mime": lambda n: setattr(self, 'mime', n.get_str_value()),
            "ocsp_status": lambda n: setattr(self, 'ocsp_status', n.get_str_value()),
            "user": lambda n: setattr(self, 'user', n.get_str_value()),
            "organization_id": lambda n: setattr(self, 'organization_id', n.get_str_value()),
            "parent_certificate_id": lambda n: setattr(self, 'parent_certificate_id', n.get_str_value()),
            "issuer": lambda n: setattr(self, 'issuer', n.get_str_value()),
            "issuer_common_name": lambda n: setattr(self, 'issuer_common_name', n.get_str_value()),
            "issuer_organization": lambda n: setattr(self, 'issuer_organization', n.get_str_value()),
            "issuer_organization_unit": lambda n: setattr(self, 'issuer_organization_unit', n.get_str_value()),
            "issuer_locality_name": lambda n: setattr(self, 'issuer_locality_name', n.get_str_value()),
            "issuer_state_or_province_name": lambda n: setattr(self, 'issuer_state_or_province_name', n.get_str_value()),
            "issuer_country_name": lambda n: setattr(self, 'issuer_country_name', n.get_str_value()),
            "issuer_postal_code": lambda n: setattr(self, 'issuer_postal_code', n.get_str_value()),
            "issuer_street_address": lambda n: setattr(self, 'issuer_street_address', n.get_str_value()),
            "issuer_title": lambda n: setattr(self, 'issuer_title', n.get_str_value()),
            "issuer_email_address": lambda n: setattr(self, 'issuer_email_address', n.get_str_value()),
            "issuer_unique_identifier": lambda n: setattr(self, 'issuer_unique_identifier', n.get_str_value()),
            "subject_common_name": lambda n: setattr(self, 'subject_common_name', n.get_str_value()),
            "subject_organization": lambda n: setattr(self, 'subject_organization', n.get_str_value()),
            "subject_organizational_unit_name": lambda n: setattr(self, 'subject_organizational_unit_name', n.get_str_value()),
            "subject_email_address": lambda n: setattr(self, 'subject_email_address', n.get_str_value()),
            "subject_unique_identifier": lambda n: setattr(self, 'subject_unique_identifier', n.get_str_value()),
            "subject_locality_name": lambda n: setattr(self, 'subject_locality_name', n.get_str_value()),
            "subject_state_or_province_name": lambda n: setattr(self, 'subject_state_or_province_name', n.get_str_value()),
            "subject_country_name": lambda n: setattr(self, 'subject_country_name', n.get_str_value()),
            "subject_postal_code": lambda n: setattr(self, 'subject_postal_code', n.get_str_value()),
            "subject_street_address": lambda n: setattr(self, 'subject_street_address', n.get_str_value()),
            "subject_title": lambda n: setattr(self, 'subject_title', n.get_str_value()),
            "subject_phone_number": lambda n: setattr(self, 'subject_phone_number', n.get_str_value()),
            "subject_business_category": lambda n: setattr(self, 'subject_business_category', n.get_str_value()),
            "subject": lambda n: setattr(self, 'subject', n.get_str_value()),
            "valid_from": lambda n: setattr(self, 'valid_from', n.get_str_value()),
            "valid_until": lambda n: setattr(self, 'valid_until', n.get_str_value()),
            "created_at": lambda n: setattr(self, 'created_at', n.get_str_value()),
            "updated_at": lambda n: setattr(self, 'updated_at', n.get_str_value()),
            "subscription_expired_at": lambda n: setattr(self, 'subscription_expired_at', n.get_str_value()),
            "subscription_renewed_at": lambda n: setattr(self, 'subscription_renewed_at', n.get_str_value()),
            "deactivated_at": lambda n: setattr(self, 'deactivated_at', n.get_str_value()),
            "deleted_at": lambda n: setattr(self, 'deleted_at', n.get_str_value()),
            "can_sync_history": lambda n: setattr(self, 'can_sync_history', n.get_bool_value()),
            "can_associate_certificates": lambda n: setattr(self, 'can_associate_certificates', n.get_bool_value()),
            "total_prepaid_movements": lambda n: setattr(self, 'total_prepaid_movements', n.get_int_value()),
            "rest_prepaid_movements": lambda n: setattr(self, 'rest_prepaid_movements', n.get_int_value()),
            "total_subscription_movements": lambda n: setattr(self, 'total_subscription_movements', n.get_int_value()),
            "rest_subscription_movements": lambda n: setattr(self, 'rest_subscription_movements', n.get_int_value()),
        }

    def serialize(self, writer: SerializationWriter) -> None:
        if not writer:
            raise TypeError("writer cannot be null.")
        writer.write_additional_data_value(self.additional_data)
