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
    from .con_clinica400_error import ConClinica400Error
    from .con_clinica401_error import ConClinica401Error
    from .con_clinica4_x_x_error import ConClinica4XXError
    from .con_clinica5_x_x_error import ConClinica5XXError
    from .con_clinica_post_response import ConClinicaPostResponse

class ConClinicaRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/imss/grupo/con-clinica
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new ConClinicaRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/imss/grupo/con-clinica?curp={curp}", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration[ConClinicaRequestBuilderPostQueryParameters]] = None) -> Optional[ConClinicaPostResponse]:
        """
        Valida si el numero de seguro social asociado a la CURP esta dado de alta y asignado en una clinica
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ConClinicaPostResponse]
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        from .con_clinica400_error import ConClinica400Error
        from .con_clinica401_error import ConClinica401Error
        from .con_clinica4_x_x_error import ConClinica4XXError
        from .con_clinica5_x_x_error import ConClinica5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": ConClinica400Error,
            "401": ConClinica401Error,
            "4XX": ConClinica4XXError,
            "5XX": ConClinica5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .con_clinica_post_response import ConClinicaPostResponse

        return await self.request_adapter.send_async(request_info, ConClinicaPostResponse, error_mapping)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration[ConClinicaRequestBuilderPostQueryParameters]] = None) -> RequestInformation:
        """
        Valida si el numero de seguro social asociado a la CURP esta dado de alta y asignado en una clinica
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> ConClinicaRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: ConClinicaRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return ConClinicaRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class ConClinicaRequestBuilderPostQueryParameters():
        """
        Valida si el numero de seguro social asociado a la CURP esta dado de alta y asignado en una clinica
        """
        # Clave Unica de Registro de poblacion
        curp: Optional[str] = None

    
    @dataclass
    class ConClinicaRequestBuilderPostRequestConfiguration(RequestConfiguration[ConClinicaRequestBuilderPostQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    
