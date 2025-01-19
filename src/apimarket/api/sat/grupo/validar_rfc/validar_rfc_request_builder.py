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
    from .validar_rfc400_error import ValidarRfc400Error
    from .validar_rfc401_error import ValidarRfc401Error
    from .validar_rfc404_error import ValidarRfc404Error
    from .validar_rfc4_x_x_error import ValidarRfc4XXError
    from .validar_rfc5_x_x_error import ValidarRfc5XXError
    from .validar_rfc_post_response import ValidarRfcPostResponse

class ValidarRfcRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/sat/grupo/validar-rfc
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new ValidarRfcRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/sat/grupo/validar-rfc{?rfc*}", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration[ValidarRfcRequestBuilderPostQueryParameters]] = None) -> Optional[ValidarRfcPostResponse]:
        """
        Valida el registro de un Registro Federal de Contribuyentes (RFC) ante el Servicio de Administracion Tributaria (SAT)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ValidarRfcPostResponse]
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        from .validar_rfc400_error import ValidarRfc400Error
        from .validar_rfc401_error import ValidarRfc401Error
        from .validar_rfc404_error import ValidarRfc404Error
        from .validar_rfc4_x_x_error import ValidarRfc4XXError
        from .validar_rfc5_x_x_error import ValidarRfc5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": ValidarRfc400Error,
            "401": ValidarRfc401Error,
            "404": ValidarRfc404Error,
            "4XX": ValidarRfc4XXError,
            "5XX": ValidarRfc5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .validar_rfc_post_response import ValidarRfcPostResponse

        return await self.request_adapter.send_async(request_info, ValidarRfcPostResponse, error_mapping)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration[ValidarRfcRequestBuilderPostQueryParameters]] = None) -> RequestInformation:
        """
        Valida el registro de un Registro Federal de Contribuyentes (RFC) ante el Servicio de Administracion Tributaria (SAT)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> ValidarRfcRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: ValidarRfcRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return ValidarRfcRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class ValidarRfcRequestBuilderPostQueryParameters():
        """
        Valida el registro de un Registro Federal de Contribuyentes (RFC) ante el Servicio de Administracion Tributaria (SAT)
        """
        # Registro Federal de contribuyentes
        rfc: Optional[str] = None

    
    @dataclass
    class ValidarRfcRequestBuilderPostRequestConfiguration(RequestConfiguration[ValidarRfcRequestBuilderPostQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

