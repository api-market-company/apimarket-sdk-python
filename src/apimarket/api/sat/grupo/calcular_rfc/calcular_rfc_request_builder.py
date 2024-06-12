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
    from .calcular_rfc400_error import CalcularRfc400Error
    from .calcular_rfc401_error import CalcularRfc401Error
    from .calcular_rfc4_x_x_error import CalcularRfc4XXError
    from .calcular_rfc5_x_x_error import CalcularRfc5XXError
    from .calcular_rfc_post_response import CalcularRfcPostResponse

class CalcularRfcRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/sat/grupo/calcular-rfc
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new CalcularRfcRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/sat/grupo/calcular-rfc?nombres={nombres}{&anoNacimiento*,diaNacimiento*,materno*,mesNacimiento*,paterno*}", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration[CalcularRfcRequestBuilderPostQueryParameters]] = None) -> Optional[CalcularRfcPostResponse]:
        """
        Valida la cedula profesional enviada en la base de datos oficial del Registro Nacional de Profesionistas,_Nota: no se muestran resultados de cedulas en proceso de titulacion._
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[CalcularRfcPostResponse]
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        from .calcular_rfc400_error import CalcularRfc400Error
        from .calcular_rfc401_error import CalcularRfc401Error
        from .calcular_rfc4_x_x_error import CalcularRfc4XXError
        from .calcular_rfc5_x_x_error import CalcularRfc5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": CalcularRfc400Error,
            "401": CalcularRfc401Error,
            "4XX": CalcularRfc4XXError,
            "5XX": CalcularRfc5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .calcular_rfc_post_response import CalcularRfcPostResponse

        return await self.request_adapter.send_async(request_info, CalcularRfcPostResponse, error_mapping)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration[CalcularRfcRequestBuilderPostQueryParameters]] = None) -> RequestInformation:
        """
        Valida la cedula profesional enviada en la base de datos oficial del Registro Nacional de Profesionistas,_Nota: no se muestran resultados de cedulas en proceso de titulacion._
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> CalcularRfcRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: CalcularRfcRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return CalcularRfcRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class CalcularRfcRequestBuilderPostQueryParameters():
        """
        Valida la cedula profesional enviada en la base de datos oficial del Registro Nacional de Profesionistas,_Nota: no se muestran resultados de cedulas en proceso de titulacion._
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
            return original_name
        
        ano_nacimiento: Optional[int] = None

        dia_nacimiento: Optional[int] = None

        materno: Optional[str] = None

        mes_nacimiento: Optional[int] = None

        # NOMBRE COMPLETO
        nombres: Optional[str] = None

        paterno: Optional[str] = None

    
    @dataclass
    class CalcularRfcRequestBuilderPostRequestConfiguration(RequestConfiguration[CalcularRfcRequestBuilderPostQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

