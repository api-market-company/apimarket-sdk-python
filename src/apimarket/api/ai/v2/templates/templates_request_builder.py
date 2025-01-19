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
    from .templates400_error import Templates400Error
    from .templates401_error import Templates401Error
    from .templates4_x_x_error import Templates4XXError
    from .templates500_error import Templates500Error
    from .templates5_x_x_error import Templates5XXError
    from .templates_post_response import TemplatesPostResponse
    from .templates_put_response import TemplatesPutResponse

class TemplatesRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/ai/v2/templates
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new TemplatesRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/ai/v2/templates", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[TemplatesPostResponse]:
        """
        Genera PDFs, imagenes o Excel desde un template en HTML, Markdown o Docx.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[TemplatesPostResponse]
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        from .templates400_error import Templates400Error
        from .templates401_error import Templates401Error
        from .templates4_x_x_error import Templates4XXError
        from .templates500_error import Templates500Error
        from .templates5_x_x_error import Templates5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": Templates400Error,
            "401": Templates401Error,
            "4XX": Templates4XXError,
            "500": Templates500Error,
            "5XX": Templates5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .templates_post_response import TemplatesPostResponse

        return await self.request_adapter.send_async(request_info, TemplatesPostResponse, error_mapping)
    
    async def put(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[TemplatesPutResponse]:
        """
        Actualiza el template. Puede ser HTML, Markdown o Docx.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[TemplatesPutResponse]
        """
        request_info = self.to_put_request_information(
            request_configuration
        )
        from .templates400_error import Templates400Error
        from .templates401_error import Templates401Error
        from .templates4_x_x_error import Templates4XXError
        from .templates500_error import Templates500Error
        from .templates5_x_x_error import Templates5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": Templates400Error,
            "401": Templates401Error,
            "4XX": Templates4XXError,
            "500": Templates500Error,
            "5XX": Templates5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .templates_put_response import TemplatesPutResponse

        return await self.request_adapter.send_async(request_info, TemplatesPutResponse, error_mapping)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Genera PDFs, imagenes o Excel desde un template en HTML, Markdown o Docx.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_put_request_information(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Actualiza el template. Puede ser HTML, Markdown o Docx.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.PUT, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> TemplatesRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: TemplatesRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return TemplatesRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class TemplatesRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    
    @dataclass
    class TemplatesRequestBuilderPutRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

