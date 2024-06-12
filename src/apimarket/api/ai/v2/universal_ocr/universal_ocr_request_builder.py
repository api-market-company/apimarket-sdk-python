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
    from .universal_ocr400_error import UniversalOcr400Error
    from .universal_ocr401_error import UniversalOcr401Error
    from .universal_ocr4_x_x_error import UniversalOcr4XXError
    from .universal_ocr5_x_x_error import UniversalOcr5XXError
    from .universal_ocr_post_request_body import UniversalOcrPostRequestBody

class UniversalOcrRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/ai/v2/universal-ocr
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new UniversalOcrRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/ai/v2/universal-ocr", path_parameters)
    
    async def post(self,body: UniversalOcrPostRequestBody, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> bytes:
        """
        Transforma tus imágenes y documentos escaneados en texto editable y dejar de perder tiempo hoy mismo. Este es un modelo de IA propio, no usamos servicios de terceros.
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: bytes
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        from .universal_ocr400_error import UniversalOcr400Error
        from .universal_ocr401_error import UniversalOcr401Error
        from .universal_ocr4_x_x_error import UniversalOcr4XXError
        from .universal_ocr5_x_x_error import UniversalOcr5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": UniversalOcr400Error,
            "401": UniversalOcr401Error,
            "4XX": UniversalOcr4XXError,
            "5XX": UniversalOcr5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_primitive_async(request_info, "bytes", error_mapping)
    
    def to_post_request_information(self,body: UniversalOcrPostRequestBody, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Transforma tus imágenes y documentos escaneados en texto editable y dejar de perder tiempo hoy mismo. Este es un modelo de IA propio, no usamos servicios de terceros.
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_parsable(self.request_adapter, "multipart/form-data", body)
        return request_info
    
    def with_url(self,raw_url: str) -> UniversalOcrRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: UniversalOcrRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return UniversalOcrRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class UniversalOcrRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

