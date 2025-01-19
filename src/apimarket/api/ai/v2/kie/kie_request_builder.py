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
    from .kie400_error import Kie400Error
    from .kie401_error import Kie401Error
    from .kie4_x_x_error import Kie4XXError
    from .kie5_x_x_error import Kie5XXError
    from .kie_post_request_body import KiePostRequestBody

class KieRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/ai/v2/kie
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new KieRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/ai/v2/kie", path_parameters)
    
    async def post(self,body: KiePostRequestBody, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> bytes:
        """
        OCR de documentos de identidad
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: bytes
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        from .kie400_error import Kie400Error
        from .kie401_error import Kie401Error
        from .kie4_x_x_error import Kie4XXError
        from .kie5_x_x_error import Kie5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": Kie400Error,
            "401": Kie401Error,
            "4XX": Kie4XXError,
            "5XX": Kie5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_primitive_async(request_info, "bytes", error_mapping)
    
    def to_post_request_information(self,body: KiePostRequestBody, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        OCR de documentos de identidad
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
    
    def with_url(self,raw_url: str) -> KieRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: KieRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return KieRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class KieRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

