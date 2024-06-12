from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_abstractions.default_query_parameters import QueryParameters
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.method import Method
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.request_option import RequestOption
from kiota_abstractions.serialization import Parsable, ParsableFactory
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union
from warnings import warn

if TYPE_CHECKING:
    from .capturar_movimientos_afiliatorios400_error import CapturarMovimientosAfiliatorios400Error
    from .capturar_movimientos_afiliatorios401_error import CapturarMovimientosAfiliatorios401Error
    from .capturar_movimientos_afiliatorios4_x_x_error import CapturarMovimientosAfiliatorios4XXError
    from .capturar_movimientos_afiliatorios5_x_x_error import CapturarMovimientosAfiliatorios5XXError
    from .capturar_movimientos_afiliatorios_post_request_body import CapturarMovimientosAfiliatoriosPostRequestBody

class CapturarMovimientosAfiliatoriosRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/imss/grupo/idse/capturar-movimientos-afiliatorios
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new CapturarMovimientosAfiliatoriosRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/imss/grupo/idse/capturar-movimientos-afiliatorios", path_parameters)
    
    async def post(self,body: CapturarMovimientosAfiliatoriosPostRequestBody, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[str]:
        """
        Genera los movimientos afiliatorios de tus trabajadores ante el IMSS. Olvidate de DispMag y trabaja con JSON.
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[str]
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        from .capturar_movimientos_afiliatorios400_error import CapturarMovimientosAfiliatorios400Error
        from .capturar_movimientos_afiliatorios401_error import CapturarMovimientosAfiliatorios401Error
        from .capturar_movimientos_afiliatorios4_x_x_error import CapturarMovimientosAfiliatorios4XXError
        from .capturar_movimientos_afiliatorios5_x_x_error import CapturarMovimientosAfiliatorios5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": CapturarMovimientosAfiliatorios400Error,
            "401": CapturarMovimientosAfiliatorios401Error,
            "4XX": CapturarMovimientosAfiliatorios4XXError,
            "5XX": CapturarMovimientosAfiliatorios5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_primitive_async(request_info, "str", error_mapping)
    
    def to_post_request_information(self,body: CapturarMovimientosAfiliatoriosPostRequestBody, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Genera los movimientos afiliatorios de tus trabajadores ante el IMSS. Olvidate de DispMag y trabaja con JSON.
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_parsable(self.request_adapter, "application/json", body)
        return request_info
    
    def with_url(self,raw_url: str) -> CapturarMovimientosAfiliatoriosRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: CapturarMovimientosAfiliatoriosRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return CapturarMovimientosAfiliatoriosRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class CapturarMovimientosAfiliatoriosRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

