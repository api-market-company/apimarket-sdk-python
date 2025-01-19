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
    from .obtener_acta_de_nacimiento400_error import ObtenerActaDeNacimiento400Error
    from .obtener_acta_de_nacimiento401_error import ObtenerActaDeNacimiento401Error
    from .obtener_acta_de_nacimiento404_error import ObtenerActaDeNacimiento404Error
    from .obtener_acta_de_nacimiento4_x_x_error import ObtenerActaDeNacimiento4XXError
    from .obtener_acta_de_nacimiento5_x_x_error import ObtenerActaDeNacimiento5XXError

class ObtenerActaDeNacimientoRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/renapo/grupo/obtener-acta-de-nacimiento
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new ObtenerActaDeNacimientoRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/renapo/grupo/obtener-acta-de-nacimiento?curp={curp}", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration[ObtenerActaDeNacimientoRequestBuilderPostQueryParameters]] = None) -> bytes:
        """
        Obtén una copia certifcada vía una API REST para la obtención y validación del acta de nacimiento.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: bytes
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        from .obtener_acta_de_nacimiento400_error import ObtenerActaDeNacimiento400Error
        from .obtener_acta_de_nacimiento401_error import ObtenerActaDeNacimiento401Error
        from .obtener_acta_de_nacimiento404_error import ObtenerActaDeNacimiento404Error
        from .obtener_acta_de_nacimiento4_x_x_error import ObtenerActaDeNacimiento4XXError
        from .obtener_acta_de_nacimiento5_x_x_error import ObtenerActaDeNacimiento5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": ObtenerActaDeNacimiento400Error,
            "401": ObtenerActaDeNacimiento401Error,
            "404": ObtenerActaDeNacimiento404Error,
            "4XX": ObtenerActaDeNacimiento4XXError,
            "5XX": ObtenerActaDeNacimiento5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_primitive_async(request_info, "bytes", error_mapping)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration[ObtenerActaDeNacimientoRequestBuilderPostQueryParameters]] = None) -> RequestInformation:
        """
        Obtén una copia certifcada vía una API REST para la obtención y validación del acta de nacimiento.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> ObtenerActaDeNacimientoRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: ObtenerActaDeNacimientoRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return ObtenerActaDeNacimientoRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class ObtenerActaDeNacimientoRequestBuilderPostQueryParameters():
        """
        Obtén una copia certifcada vía una API REST para la obtención y validación del acta de nacimiento.
        """
        # Clave Unica de Registro de Poblacion
        curp: Optional[str] = None

    
    @dataclass
    class ObtenerActaDeNacimientoRequestBuilderPostRequestConfiguration(RequestConfiguration[ObtenerActaDeNacimientoRequestBuilderPostQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

