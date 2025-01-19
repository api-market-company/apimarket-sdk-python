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
    from .registros_patronales400_error import RegistrosPatronales400Error
    from .registros_patronales401_error import RegistrosPatronales401Error
    from .registros_patronales4_x_x_error import RegistrosPatronales4XXError
    from .registros_patronales5_x_x_error import RegistrosPatronales5XXError
    from .registros_patronales_post_request_body import RegistrosPatronalesPostRequestBody

class RegistrosPatronalesRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/imss/grupo/idse/registros-patronales
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new RegistrosPatronalesRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/imss/grupo/idse/registros-patronales", path_parameters)
    
    async def post(self,body: RegistrosPatronalesPostRequestBody, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[str]:
        """
        IDSE IMSS: Este endpoint te envía  los registros patronales asociados al certificado mediante webhook.
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[str]
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        from .registros_patronales400_error import RegistrosPatronales400Error
        from .registros_patronales401_error import RegistrosPatronales401Error
        from .registros_patronales4_x_x_error import RegistrosPatronales4XXError
        from .registros_patronales5_x_x_error import RegistrosPatronales5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": RegistrosPatronales400Error,
            "401": RegistrosPatronales401Error,
            "4XX": RegistrosPatronales4XXError,
            "5XX": RegistrosPatronales5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_primitive_async(request_info, "str", error_mapping)
    
    def to_post_request_information(self,body: RegistrosPatronalesPostRequestBody, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        IDSE IMSS: Este endpoint te envía  los registros patronales asociados al certificado mediante webhook.
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
    
    def with_url(self,raw_url: str) -> RegistrosPatronalesRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: RegistrosPatronalesRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return RegistrosPatronalesRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class RegistrosPatronalesRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

