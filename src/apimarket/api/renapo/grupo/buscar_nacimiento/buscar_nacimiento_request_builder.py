from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.method import Method
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.serialization import Parsable, ParsableFactory
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .buscar_nacimiento400_error import BuscarNacimiento400Error
    from .buscar_nacimiento401_error import BuscarNacimiento401Error
    from .buscar_nacimiento4_x_x_error import BuscarNacimiento4XXError
    from .buscar_nacimiento5_x_x_error import BuscarNacimiento5XXError
    from .buscar_nacimiento_post_response import BuscarNacimientoPostResponse

class BuscarNacimientoRequestBuilder(BaseRequestBuilder):
    def __init__(self, request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        super().__init__(request_adapter, "{+baseurl}/api/renapo/grupo/buscar-nacimiento?curp={curp}", path_parameters)

    async def post(self, request_configuration: Optional[RequestConfiguration] = None) -> Optional[BuscarNacimientoPostResponse]:
        request_info = self.to_post_request_information(request_configuration)
        from .buscar_nacimiento400_error import BuscarNacimiento400Error
        from .buscar_nacimiento401_error import BuscarNacimiento401Error
        from .buscar_nacimiento4_x_x_error import BuscarNacimiento4XXError
        from .buscar_nacimiento5_x_x_error import BuscarNacimiento5XXError
        error_mapping: Dict[str, ParsableFactory] = {
            "400": BuscarNacimiento400Error,
            "401": BuscarNacimiento401Error,
            "4XX": BuscarNacimiento4XXError,
            "5XX": BuscarNacimiento5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null")
        from .buscar_nacimiento_post_response import BuscarNacimientoPostResponse
        return await self.request_adapter.send_async(request_info, BuscarNacimientoPostResponse, error_mapping)

    def to_post_request_information(self, request_configuration: Optional[RequestConfiguration] = None) -> RequestInformation:
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info

    def with_url(self, raw_url: str) -> BuscarNacimientoRequestBuilder:
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return BuscarNacimientoRequestBuilder(self.request_adapter, raw_url)

    @dataclass
    class BuscarNacimientoRequestBuilderPostQueryParameters():
        curp: Optional[str] = None
