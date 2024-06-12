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
    from .obtener_rfc400_error import ObtenerRfc400Error
    from .obtener_rfc401_error import ObtenerRfc401Error
    from .obtener_rfc404_error import ObtenerRfc404Error
    from .obtener_rfc4_x_x_error import ObtenerRfc4XXError
    from .obtener_rfc5_x_x_error import ObtenerRfc5XXError
    from .obtener_rfc_post_response import ObtenerRfcPostResponse

class ObtenerRfcRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/sat/grupo/obtener-rfc
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new ObtenerRfcRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/sat/grupo/obtener-rfc{?curp*}", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration[ObtenerRfcRequestBuilderPostQueryParameters]] = None) -> Optional[ObtenerRfcPostResponse]:
        """
        Obtiene el RFC Oficial registrado en el SAT, mediante el envio de curp_Nota: no se muestran resultados de RFC sin registro_
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ObtenerRfcPostResponse]
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        from .obtener_rfc400_error import ObtenerRfc400Error
        from .obtener_rfc401_error import ObtenerRfc401Error
        from .obtener_rfc404_error import ObtenerRfc404Error
        from .obtener_rfc4_x_x_error import ObtenerRfc4XXError
        from .obtener_rfc5_x_x_error import ObtenerRfc5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": ObtenerRfc400Error,
            "401": ObtenerRfc401Error,
            "404": ObtenerRfc404Error,
            "4XX": ObtenerRfc4XXError,
            "5XX": ObtenerRfc5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .obtener_rfc_post_response import ObtenerRfcPostResponse

        return await self.request_adapter.send_async(request_info, ObtenerRfcPostResponse, error_mapping)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration[ObtenerRfcRequestBuilderPostQueryParameters]] = None) -> RequestInformation:
        """
        Obtiene el RFC Oficial registrado en el SAT, mediante el envio de curp_Nota: no se muestran resultados de RFC sin registro_
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> ObtenerRfcRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: ObtenerRfcRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return ObtenerRfcRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class ObtenerRfcRequestBuilderPostQueryParameters():
        """
        Obtiene el RFC Oficial registrado en el SAT, mediante el envio de curp_Nota: no se muestran resultados de RFC sin registro_
        """
        # Clave Unica de Registro de Poblacion
        curp: Optional[str] = None

    
    @dataclass
    class ObtenerRfcRequestBuilderPostRequestConfiguration(RequestConfiguration[ObtenerRfcRequestBuilderPostQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

