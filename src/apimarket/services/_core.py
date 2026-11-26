"""Capa declarativa de servicios.

Cada servicio es una función decorada con :func:`service` que valida sus
argumentos y devuelve un :class:`Call`. El decorador envía la petición con el
adaptador de Kiota que configura ``apimarket.assemble()`` y registra el servicio
para que la CLI lo exponga sin código adicional.

Las respuestas JSON se devuelven como ``dict``; cualquier otro contenido, como
``bytes``.
"""
import functools
import inspect
import json
import os
from dataclasses import dataclass, field
from typing import Any, BinaryIO, Callable, Dict, Optional, Union
from urllib.parse import quote, urlencode

import httpx
from kink import di
from kiota_abstractions.api_error import APIError
from kiota_abstractions.headers_collection import HeadersCollection
from kiota_abstractions.method import Method
from kiota_abstractions.native_response_handler import NativeResponseHandler
from kiota_abstractions.request_information import RequestInformation
from kiota_http.middleware.options import ResponseHandlerOption, RetryHandlerOption

from apimarket.api_market_client import ApiMarketClient
from apimarket.errors import ErrorCode, api_error_code
from apimarket.rules import boolean, load_file, required
from apimarket.validations import InvalidParameterError

#: Ruta a un archivo, su contenido o un objeto de archivo abierto en binario.
FileInput = Union[str, "os.PathLike[str]", bytes, BinaryIO]


class ApiMarketError(APIError):
    """La API respondió con un código de error.

    Hereda de ``APIError`` y expone los mismos campos que los errores tipados de
    los demás endpoints: ``message``, ``status``, ``success``,
    ``codigo_validacion``, ``data``, ``additional_data`` y
    ``response_status_code``. ``body`` contiene la respuesta completa.
    """

    _FIELDS = ("message", "status", "success", "codigoValidacion", "data")

    def __init__(self, status_code: int, body: Any, headers: Optional[dict] = None):
        payload = body if isinstance(body, dict) else {}
        message = payload.get("message") or f"La API respondió con el código {status_code}."
        super().__init__(message, status_code, headers or {})
        self.body = body
        self.status: Optional[int] = payload.get("status")
        self.success: Optional[bool] = payload.get("success")
        self.codigo_validacion: Optional[str] = payload.get("codigoValidacion")
        self.data: Any = payload.get("data")
        self.additional_data = {key: value for key, value in payload.items() if key not in self._FIELDS}
        # Un HTTP 200 puede traer el estado de error solo en el cuerpo.
        self.code = api_error_code(status_code if status_code >= 400 else self.status)


@dataclass
class Call:
    """Datos de una petición. Los valores ``None`` se omiten."""
    path_params: Dict[str, Any] = field(default_factory=dict)
    query: Dict[str, Any] = field(default_factory=dict)
    json: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None
    files: Optional[Dict[str, FileInput]] = None
    headers: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ServiceSpec:
    group: str
    command: str
    method: str
    path: str
    function: Callable
    retry: bool

    @property
    def signature(self) -> inspect.Signature:
        return inspect.signature(self.function)

    @property
    def summary(self) -> str:
        return (inspect.getdoc(self.function) or "").split("\n")[0]


REGISTRY: "list[ServiceSpec]" = []


def service(group: str, command: str, path: str, method: str = "POST", retry: bool = True):
    """Declara un servicio de API Market.

    ``retry=False`` desactiva los reintentos automáticos de Kiota (429, 503 y
    504). Úselo en operaciones que crean o modifican algo.
    """

    def decorator(build: Callable[..., Call]) -> Callable[..., Any]:
        @functools.wraps(build)
        def wrapper(*args, **kwargs):
            from apimarket import choice_process_scheduler, ensure_api_key

            # Las validaciones locales corren aquí, antes de abrir la conexión.
            call = build(*args, **kwargs)
            _check_path_params(call)
            ensure_api_key()
            return choice_process_scheduler(lambda: _send(spec, call))()

        spec = ServiceSpec(group, command, method, path, wrapper, retry)
        REGISTRY.append(spec)
        return wrapper

    return decorator


def reset_header(reset: bool) -> Dict[str, str]:
    """Encabezado que pide a la API ignorar su caché."""
    return {"x-reset": "true"} if boolean("reset", reset) else {}


def compact(values: Dict[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in values.items() if value is not None}


#: Primeros bytes de los formatos que la API distingue por la extensión.
def _check_path_params(call: Call) -> None:
    for name, value in call.path_params.items():
        required(**{name: value})
        if str(value) in (".", ".."):
            raise InvalidParameterError.of(name, "PATH", f"El parámetro '{name}' no puede ser '{value}'.")


def _build_url(base_url: str, spec: ServiceSpec, call: Call) -> str:
    path = spec.path
    for name, value in call.path_params.items():
        path = path.replace("{%s}" % name, quote(str(value), safe=""))
    url = base_url.rstrip("/") + path
    query = compact(call.query)
    if query:
        url += "?" + urlencode(query)
    return url


def _build_request(base_url: str, spec: ServiceSpec, call: Call) -> RequestInformation:
    request = RequestInformation()
    request.http_method = Method[spec.method]
    request.url = _build_url(base_url, spec, call)
    request.headers.add_all(di[HeadersCollection])
    for name, value in call.headers.items():
        request.headers.try_add(name, value)

    if call.files is not None or call.data is not None:
        loaded = {name: load_file(name, value) for name, value in compact(call.files or {}).items()}
        files = {name: (item.name, item.content, item.mime) for name, item in loaded.items()}
        # httpx arma el cuerpo multipart y su encabezado con el delimitador.
        encoded = httpx.Request("POST", base_url, data=compact(call.data or {}), files=files)
        request.content = encoded.read()
        request.headers.try_add("Content-Type", encoded.headers["Content-Type"])
    elif call.json is not None:
        request.content = json.dumps(compact(call.json)).encode("utf-8")
        request.headers.try_add("Content-Type", "application/json")

    options = [ResponseHandlerOption(NativeResponseHandler())]
    if not spec.retry:
        options.append(RetryHandlerOption(should_retry=False))
    request.add_request_options(options)
    return request


def _decode(response: httpx.Response) -> Any:
    if not response.content:
        return None
    if "json" in response.headers.get("content-type", ""):
        try:
            return response.json()
        except ValueError:
            error = ApiMarketError(response.status_code, None, dict(response.headers))
            error.message = "La API respondió un JSON que no se puede leer."
            error.code = ErrorCode.API_RESPONSE_INVALID
            raise error
    return response.content


async def _send(spec: ServiceSpec, call: Call) -> Any:
    adapter = di[ApiMarketClient].request_adapter
    request = _build_request(adapter.base_url, spec, call)
    response = await adapter.send_primitive_async(request, "bytes", None)
    body = _decode(response)
    status = body.get("status") if isinstance(body, dict) else None
    # La API a veces responde HTTP 200 y reporta la falla del proveedor en "status".
    if not response.is_success or (isinstance(status, int) and status >= 500):
        raise ApiMarketError(response.status_code, body, dict(response.headers))
    return body
