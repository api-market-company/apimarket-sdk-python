"""Reglas de validación reutilizables. Reflejan las reglas de la API.

Cada función lanza una subclase de ``ValidationError`` o devuelve el valor.
"""
import json
import mimetypes
import os
import re
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from apimarket.validations import (InvalidFileError, InvalidParameterError,
                                   validate_credit_number, validate_curp, validate_nss, validate_rfc)

_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
# La misma forma que exige la API a un webhook.
_HTTPS_URL = re.compile(
    r"^https://(?:www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_+.~#?&/=]*)$", re.I)
_CIPHER = re.compile(r"^[0-9A-Fa-f]+$")

#: Claves y abreviaturas de entidad que acepta RENAPO.
ENTITIES = tuple(f"{number:02d}" for number in (*range(1, 33), 87, 88)) + tuple(
    "AS BC BS CC CL CM CS CH DF DG GT GR HG JC MC MN MS NT NL OC PL QT QR SP SL SR TC TS TL VZ YN ZS NE".split())


def fail(name: str, reason: str, message: str):
    """Lanza ``INVALID_<NAME>_<REASON>``."""
    raise InvalidParameterError.of(name, reason, message)


def required(**values) -> None:
    """Rechaza argumentos obligatorios ausentes o vacíos."""
    for name, value in values.items():
        if value is None or (isinstance(value, (str, bytes, list, dict, tuple)) and not value) \
                or (isinstance(value, str) and not value.strip()):
            fail(name, "MISSING", f"El parámetro '{name}' es obligatorio.")


def text(name: str, value, min_length: int = 1, max_length: int = None) -> str:
    required(**{name: value})
    if not isinstance(value, str):
        fail(name, "TYPE", f"El parámetro '{name}' debe ser texto.")
    if len(value) < min_length or (max_length and len(value) > max_length):
        limits = f"al menos {min_length}" + (f" y como máximo {max_length}" if max_length else "")
        fail(name, "LENGTH", f"El parámetro '{name}' debe tener {limits} caracteres.")
    return value


def optional_text(name: str, value, max_length: int = None):
    return None if value is None else text(name, value, max_length=max_length)


def digits(name: str, value, min_length: int = 1, max_length: int = None) -> str:
    """Cadena numérica; también acepta enteros."""
    if isinstance(value, int) and not isinstance(value, bool):
        value = str(value)
    text(name, value)
    if not re.fullmatch(r"[0-9]+", value):
        fail(name, "FORMAT", f"El parámetro '{name}' solo admite dígitos.")
    if len(value) < min_length or (max_length and len(value) > max_length):
        length = str(min_length) if min_length == max_length else f"de {min_length} a {max_length}"
        fail(name, "LENGTH", f"El parámetro '{name}' debe tener {length} dígitos.")
    return value


def integer(name: str, value, minimum: int = None, maximum: int = None) -> int:
    required(**{name: value})
    if not isinstance(value, int) or isinstance(value, bool):
        fail(name, "TYPE", f"El parámetro '{name}' debe ser un número entero.")
    if (minimum is not None and value < minimum) or (maximum is not None and value > maximum):
        limits = f"estar entre {minimum} y {maximum}" if maximum is not None else f"ser {minimum} o mayor"
        fail(name, "RANGE", f"El parámetro '{name}' debe {limits}.")
    return value


def boolean(name: str, value) -> bool:
    if not isinstance(value, bool):
        fail(name, "TYPE", f"El parámetro '{name}' debe ser True o False.")
    return value


def option(name: str, value, choices, ignore_case: bool = False) -> str:
    text(name, value)
    normalized = value.strip().upper() if ignore_case else value
    if normalized not in choices:
        fail(name, "OPTION", f"El parámetro '{name}' debe ser uno de: {', '.join(choices)}.")
    return normalized


def email(name: str, value, max_length: int = 254) -> str:
    text(name, value, max_length=max_length)
    if not _EMAIL.match(value):
        fail(name, "FORMAT", f"El parámetro '{name}' no es un correo electrónico válido.")
    return value


def https_url(name: str, value, max_length: int = None) -> str:
    text(name, value, max_length=max_length)
    if not _HTTPS_URL.match(value):
        fail(name, "FORMAT", f"El parámetro '{name}' debe ser una URL https válida.")
    return value


def date(name: str, value) -> datetime:
    """Fecha en formato ISO 8601, por ejemplo ``2024-01-31``."""
    text(name, value)
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        fail(name, "FORMAT", f"El parámetro '{name}' debe ser una fecha AAAA-MM-DD.")


def uuid_text(name: str, value) -> str:
    text(name, value)
    try:
        valid = str(uuid.UUID(value)) == value.lower()
    except ValueError:
        valid = False
    if not valid:
        fail(name, "FORMAT", f"El parámetro '{name}' debe ser un UUID.")
    return value


def mapping(name: str, value) -> dict:
    required(**{name: value})
    if not isinstance(value, dict):
        fail(name, "TYPE", f"El parámetro '{name}' debe ser un objeto.")
    return value


def items(name: str, value, max_items: int = None) -> list:
    required(**{name: value})
    if not isinstance(value, (list, tuple)):
        fail(name, "TYPE", f"El parámetro '{name}' debe ser una lista.")
    if max_items and len(value) > max_items:
        fail(name, "LENGTH", f"El parámetro '{name}' admite como máximo {max_items} elementos.")
    return list(value)


def identifier(name: str, value, allow_credit: bool = False) -> str:
    """NSS, RFC, CURP y, si se permite, número de crédito."""
    text(name, value)
    if re.fullmatch(r"[0-9]{11}", value):
        validate_nss(value)
    elif allow_credit and re.fullmatch(r"[0-9]{10}", value):
        validate_credit_number(value)
    elif re.fullmatch(r"[A-ZÑ&]{3,4}[0-9]{6}[A-Z0-9]{3}", value):
        pass
    elif len(value) == 18:
        validate_curp(value)
    else:
        kinds = "NSS, RFC, CURP" + (" o número de crédito" if allow_credit else "")
        fail(name, "FORMAT", f"El parámetro '{name}' debe ser un {kinds} válido.")
    return value


def operator_filter(name: str, value) -> str:
    """Filtro con operador, por ejemplo ``eq.10001``."""
    text(name, value)
    if not re.match(r"^[a-z]+(\([a-z]+\))?\..+", value):
        fail(name, "FORMAT", f"El parámetro '{name}' debe llevar un operador, por ejemplo 'eq.valor'.")
    return value


def is_encrypted(value) -> bool:
    """Indica si el valor viene cifrado con la llave del token (hexadecimal en bloques)."""
    return isinstance(value, str) and len(value) >= 32 and len(value) % 32 == 0 and bool(_CIPHER.match(value))


def sat_credentials(rfc, ciec) -> None:
    """RFC y CIEC son opcionales; cifrados no se pueden revisar localmente."""
    if rfc is not None:
        text("rfc", rfc)
        if not is_encrypted(rfc):
            validate_rfc(rfc)
    if ciec is not None:
        text("ciec", ciec)
        if not is_encrypted(ciec):
            text("ciec", ciec, min_length=8, max_length=64)


# ---------------------------------------------------------------------------
# Archivos
# ---------------------------------------------------------------------------

_SIGNATURES = ((b"%PDF-", ".pdf"), (b"\x89PNG\r\n\x1a\n", ".png"), (b"\xff\xd8\xff", ".jpg"))
#: Tamaño máximo de una plantilla.
TEMPLATE_MAX_MEGABYTES = 500
#: Extensiones de documentos e imágenes que leen los servicios de OCR.
DOCUMENTS = (".pdf", ".png", ".jpg", ".jpeg")


@dataclass(frozen=True)
class LoadedFile:
    name: str
    content: bytes

    @property
    def mime(self) -> str:
        return mimetypes.guess_type(self.name)[0] or "application/octet-stream"


def load_file(name: str, value, extensions=None, max_megabytes: int = None) -> LoadedFile:
    """Lee una ruta, bytes u objeto de archivo y revisa su tipo y tamaño."""
    if isinstance(value, LoadedFile):
        return value
    if value is None or (isinstance(value, str) and not value):
        required(**{name: value})
    try:
        if isinstance(value, bytes):
            filename, content = name, value
        elif isinstance(value, (str, os.PathLike)):
            path = Path(value)
            filename, content = path.name, path.read_bytes()
        elif hasattr(value, "read"):
            filename = Path(str(getattr(value, "name", name))).name
            content = value.read()
        else:
            fail(name, "TYPE", f"El parámetro '{name}' debe ser una ruta, bytes o un archivo.")
    except FileNotFoundError:
        raise InvalidFileError.of(name, "FILE_NOT_FOUND", f"No existe el archivo '{value}'.")
    except OSError as error:
        raise InvalidFileError.of(name, "FILE_UNREADABLE", f"No se pudo leer '{value}': {error.strerror}.")

    if not isinstance(content, bytes):
        raise InvalidFileError.of(name, "FILE_UNREADABLE", f"El archivo '{name}' debe abrirse en modo binario.")
    if not content:
        raise InvalidFileError.of(name, "FILE_EMPTY", f"El archivo '{name}' está vacío.")
    if max_megabytes and len(content) > max_megabytes * 1024 * 1024:
        raise InvalidFileError.of(name, "FILE_SIZE",
                                  f"El archivo '{name}' supera el máximo de {max_megabytes} MB.")

    if not Path(filename).suffix:
        # La API elige cómo leer el archivo según la extensión, y los bytes no traen nombre.
        filename += next((suffix for magic, suffix in _SIGNATURES if content.startswith(magic)), "")
    if extensions and Path(filename).suffix.lower() not in extensions:
        raise InvalidFileError.of(name, "FILE_TYPE",
                                  f"El archivo '{name}' debe ser de tipo: {', '.join(extensions)}.")
    return LoadedFile(filename, content)


def template_file(name: str, value) -> LoadedFile:
    """Plantilla PDFMe: JSON con al menos una página en ``schemas``."""
    loaded = load_file(name, value, max_megabytes=TEMPLATE_MAX_MEGABYTES)
    try:
        template = json.loads(loaded.content)
    except ValueError:
        template = None
    schemas = template.get("schemas") if isinstance(template, dict) else None
    if not isinstance(schemas, list) or not schemas:
        raise InvalidFileError.of(name, "FILE_CONTENT",
                                  "La plantilla debe ser JSON con al menos una página en 'schemas'.")
    stem = loaded.name if loaded.name.lower().endswith(".json") else f"{loaded.name}.json"
    return LoadedFile(stem, loaded.content)


def csv_file(name: str, value) -> LoadedFile:
    loaded = load_file(name, value)
    suffix = Path(loaded.name).suffix.lower()
    is_text = b"\x00" not in loaded.content and not any(loaded.content.startswith(m) for m, _ in _SIGNATURES)
    if suffix not in ("", ".csv") or not is_text:
        raise InvalidFileError.of(name, "FILE_TYPE", f"El archivo '{name}' debe ser CSV.")
    return loaded if suffix else LoadedFile(f"{loaded.name}.csv", loaded.content)
