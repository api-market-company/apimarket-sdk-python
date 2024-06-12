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
    from .obtener_datos400_error import ObtenerDatos400Error
    from .obtener_datos401_error import ObtenerDatos401Error
    from .obtener_datos4_x_x_error import ObtenerDatos4XXError
    from .obtener_datos5_x_x_error import ObtenerDatos5XXError
    from .obtener_datos_post_response import ObtenerDatosPostResponse

class ObtenerDatosRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/sat/grupo/obtener-datos
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new ObtenerDatosRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/sat/grupo/obtener-datos?rfc={rfc}", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration[ObtenerDatosRequestBuilderPostQueryParameters]] = None) -> Optional[ObtenerDatosPostResponse]:
        """
        Obten la mayoria de los datos de la constancia de situacion fiscal (CIF) de personas fisicas y morales relacionadas a un RFC (Registro Federal de Contribuyentes) como nombre completo o razon social, codigo postal y regimenes inscritos en el SAT.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ObtenerDatosPostResponse]
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        from .obtener_datos400_error import ObtenerDatos400Error
        from .obtener_datos401_error import ObtenerDatos401Error
        from .obtener_datos4_x_x_error import ObtenerDatos4XXError
        from .obtener_datos5_x_x_error import ObtenerDatos5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": ObtenerDatos400Error,
            "401": ObtenerDatos401Error,
            "4XX": ObtenerDatos4XXError,
            "5XX": ObtenerDatos5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .obtener_datos_post_response import ObtenerDatosPostResponse

        return await self.request_adapter.send_async(request_info, ObtenerDatosPostResponse, error_mapping)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration[ObtenerDatosRequestBuilderPostQueryParameters]] = None) -> RequestInformation:
        """
        Obten la mayoria de los datos de la constancia de situacion fiscal (CIF) de personas fisicas y morales relacionadas a un RFC (Registro Federal de Contribuyentes) como nombre completo o razon social, codigo postal y regimenes inscritos en el SAT.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> ObtenerDatosRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: ObtenerDatosRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return ObtenerDatosRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class ObtenerDatosRequestBuilderPostQueryParameters():
        """
        Obten la mayoria de los datos de la constancia de situacion fiscal (CIF) de personas fisicas y morales relacionadas a un RFC (Registro Federal de Contribuyentes) como nombre completo o razon social, codigo postal y regimenes inscritos en el SAT.
        """
        # Registro Federal de Contribuyentes
        rfc: Optional[str] = None

    
    @dataclass
    class ObtenerDatosRequestBuilderPostRequestConfiguration(RequestConfiguration[ObtenerDatosRequestBuilderPostQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

