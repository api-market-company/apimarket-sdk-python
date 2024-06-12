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
    from .obtener_cedula400_error import ObtenerCedula400Error
    from .obtener_cedula401_error import ObtenerCedula401Error
    from .obtener_cedula404_error import ObtenerCedula404Error
    from .obtener_cedula4_x_x_error import ObtenerCedula4XXError
    from .obtener_cedula5_x_x_error import ObtenerCedula5XXError
    from .obtener_cedula_post_response import ObtenerCedulaPostResponse

class ObtenerCedulaRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/sep/grupo/obtener-cedula
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new ObtenerCedulaRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/sep/grupo/obtener-cedula?nombres={nombres}&paterno={paterno}{&materno*}", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration[ObtenerCedulaRequestBuilderPostQueryParameters]] = None) -> Optional[ObtenerCedulaPostResponse]:
        """
        Busca Cedulas relacionadas a los datos enviadas en la base de datos del **Registro Nacional de Profesionistas.**_Nota: esta busqueda no es con coincidencia exacta, mostrara todos los registros que contengan los datos enviados._
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ObtenerCedulaPostResponse]
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        from .obtener_cedula400_error import ObtenerCedula400Error
        from .obtener_cedula401_error import ObtenerCedula401Error
        from .obtener_cedula404_error import ObtenerCedula404Error
        from .obtener_cedula4_x_x_error import ObtenerCedula4XXError
        from .obtener_cedula5_x_x_error import ObtenerCedula5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": ObtenerCedula400Error,
            "401": ObtenerCedula401Error,
            "404": ObtenerCedula404Error,
            "4XX": ObtenerCedula4XXError,
            "5XX": ObtenerCedula5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .obtener_cedula_post_response import ObtenerCedulaPostResponse

        return await self.request_adapter.send_async(request_info, ObtenerCedulaPostResponse, error_mapping)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration[ObtenerCedulaRequestBuilderPostQueryParameters]] = None) -> RequestInformation:
        """
        Busca Cedulas relacionadas a los datos enviadas en la base de datos del **Registro Nacional de Profesionistas.**_Nota: esta busqueda no es con coincidencia exacta, mostrara todos los registros que contengan los datos enviados._
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> ObtenerCedulaRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: ObtenerCedulaRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return ObtenerCedulaRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class ObtenerCedulaRequestBuilderPostQueryParameters():
        """
        Busca Cedulas relacionadas a los datos enviadas en la base de datos del **Registro Nacional de Profesionistas.**_Nota: esta busqueda no es con coincidencia exacta, mostrara todos los registros que contengan los datos enviados._
        """
        # [OPCIONAL]
        materno: Optional[str] = None

        nombres: Optional[str] = None

        paterno: Optional[str] = None

    
    @dataclass
    class ObtenerCedulaRequestBuilderPostRequestConfiguration(RequestConfiguration[ObtenerCedulaRequestBuilderPostQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

