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
    from .obtener_curp400_error import ObtenerCurp400Error
    from .obtener_curp401_error import ObtenerCurp401Error
    from .obtener_curp4_x_x_error import ObtenerCurp4XXError
    from .obtener_curp5_x_x_error import ObtenerCurp5XXError
    from .obtener_curp_post_response import ObtenerCurpPostResponse

class ObtenerCurpRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/renapo/grupo/obtener-curp
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new ObtenerCurpRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/renapo/grupo/obtener-curp{?anoNacimiento*,claveEntidad*,diaNacimiento*,materno*,mesNacimiento*,nombres*,paterno*,sexo*}", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration[ObtenerCurpRequestBuilderPostQueryParameters]] = None) -> Optional[ObtenerCurpPostResponse]:
        """
        Obten la CURP de tus usuarios a traves del envio de sus datos.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ObtenerCurpPostResponse]
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        from .obtener_curp400_error import ObtenerCurp400Error
        from .obtener_curp401_error import ObtenerCurp401Error
        from .obtener_curp4_x_x_error import ObtenerCurp4XXError
        from .obtener_curp5_x_x_error import ObtenerCurp5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": ObtenerCurp400Error,
            "401": ObtenerCurp401Error,
            "4XX": ObtenerCurp4XXError,
            "5XX": ObtenerCurp5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .obtener_curp_post_response import ObtenerCurpPostResponse

        return await self.request_adapter.send_async(request_info, ObtenerCurpPostResponse, error_mapping)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration[ObtenerCurpRequestBuilderPostQueryParameters]] = None) -> RequestInformation:
        """
        Obten la CURP de tus usuarios a traves del envio de sus datos.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> ObtenerCurpRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: ObtenerCurpRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return ObtenerCurpRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class ObtenerCurpRequestBuilderPostQueryParameters():
        """
        Obten la CURP de tus usuarios a traves del envio de sus datos.
        """
        def get_query_parameter(self,original_name: str) -> str:
            """
            Maps the query parameters names to their encoded names for the URI template parsing.
            param original_name: The original query parameter name in the class.
            Returns: str
            """
            if not original_name:
                raise TypeError("original_name cannot be null.")
            if original_name == "ano_nacimiento":
                return "anoNacimiento"
            if original_name == "clave_entidad":
                return "claveEntidad"
            if original_name == "dia_nacimiento":
                return "diaNacimiento"
            if original_name == "mes_nacimiento":
                return "mesNacimiento"
            if original_name == "materno":
                return "materno"
            if original_name == "nombres":
                return "nombres"
            if original_name == "paterno":
                return "paterno"
            if original_name == "sexo":
                return "sexo"
            return original_name
        
        ano_nacimiento: Optional[int] = None

        clave_entidad: Optional[int] = None

        dia_nacimiento: Optional[int] = None

        materno: Optional[str] = None

        mes_nacimiento: Optional[int] = None

        nombres: Optional[str] = None

        paterno: Optional[str] = None

        sexo: Optional[str] = None

    
    @dataclass
    class ObtenerCurpRequestBuilderPostRequestConfiguration(RequestConfiguration[ObtenerCurpRequestBuilderPostQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

