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
    from .parse_csf400_error import ParseCsf400Error
    from .parse_csf401_error import ParseCsf401Error
    from .parse_csf404_error import ParseCsf404Error
    from .parse_csf4_x_x_error import ParseCsf4XXError
    from .parse_csf5_x_x_error import ParseCsf5XXError
    from .parse_csf_post_response import ParseCsfPostResponse

class ParseCsfRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/sat/grupo/parse-csf
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new ParseCsfRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/sat/grupo/parse-csf", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[ParseCsfPostResponse]:
        """
        Obten todo el contenido en formato JSON de una Constancia de Situacion Fiscal emitida por el Servicio de Administracion Tributaria (SAT)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ParseCsfPostResponse]
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        from .parse_csf400_error import ParseCsf400Error
        from .parse_csf401_error import ParseCsf401Error
        from .parse_csf404_error import ParseCsf404Error
        from .parse_csf4_x_x_error import ParseCsf4XXError
        from .parse_csf5_x_x_error import ParseCsf5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": ParseCsf400Error,
            "401": ParseCsf401Error,
            "404": ParseCsf404Error,
            "4XX": ParseCsf4XXError,
            "5XX": ParseCsf5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .parse_csf_post_response import ParseCsfPostResponse

        return await self.request_adapter.send_async(request_info, ParseCsfPostResponse, error_mapping)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Obten todo el contenido en formato JSON de una Constancia de Situacion Fiscal emitida por el Servicio de Administracion Tributaria (SAT)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> ParseCsfRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: ParseCsfRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return ParseCsfRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class ParseCsfRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

