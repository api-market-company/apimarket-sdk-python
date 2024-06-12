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
    from .validar_cedula400_error import ValidarCedula400Error
    from .validar_cedula401_error import ValidarCedula401Error
    from .validar_cedula4_x_x_error import ValidarCedula4XXError
    from .validar_cedula5_x_x_error import ValidarCedula5XXError
    from .validar_cedula_post_response import ValidarCedulaPostResponse

class ValidarCedulaRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/sep/grupo/validar-cedula
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new ValidarCedulaRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/sep/grupo/validar-cedula?cedula={cedula}", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration[ValidarCedulaRequestBuilderPostQueryParameters]] = None) -> Optional[ValidarCedulaPostResponse]:
        """
        Valida la cedula profesional enviada en la base de datos oficial del Registro Nacional de Profesionistas,
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ValidarCedulaPostResponse]
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        from .validar_cedula400_error import ValidarCedula400Error
        from .validar_cedula401_error import ValidarCedula401Error
        from .validar_cedula4_x_x_error import ValidarCedula4XXError
        from .validar_cedula5_x_x_error import ValidarCedula5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": ValidarCedula400Error,
            "401": ValidarCedula401Error,
            "4XX": ValidarCedula4XXError,
            "5XX": ValidarCedula5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .validar_cedula_post_response import ValidarCedulaPostResponse

        return await self.request_adapter.send_async(request_info, ValidarCedulaPostResponse, error_mapping)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration[ValidarCedulaRequestBuilderPostQueryParameters]] = None) -> RequestInformation:
        """
        Valida la cedula profesional enviada en la base de datos oficial del Registro Nacional de Profesionistas,
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> ValidarCedulaRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: ValidarCedulaRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return ValidarCedulaRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class ValidarCedulaRequestBuilderPostQueryParameters():
        """
        Valida la cedula profesional enviada en la base de datos oficial del Registro Nacional de Profesionistas,
        """
        # Cedula profesional
        cedula: Optional[int] = None

    
    @dataclass
    class ValidarCedulaRequestBuilderPostRequestConfiguration(RequestConfiguration[ValidarCedulaRequestBuilderPostQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

