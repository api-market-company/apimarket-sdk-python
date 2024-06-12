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
    from .....models.curp_a_p_i_response import CurpAPIResponse
    from .curp_a_p_i_response400_error import CurpAPIResponse400Error
    from .curp_a_p_i_response401_error import CurpAPIResponse401Error
    from .curp_a_p_i_response404_error import CurpAPIResponse404Error
    from .curp_a_p_i_response4_x_x_error import CurpAPIResponse4XXError
    from .curp_a_p_i_response5_x_x_error import CurpAPIResponse5XXError

class ValidaCurpRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/renapo/grupo/valida-curp
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new ValidaCurpRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/renapo/grupo/valida-curp?curp={curp}", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration[ValidaCurpRequestBuilderPostQueryParameters]] = None) -> Optional[CurpAPIResponse]:
        """
        Valida CURP API, es una API REST para la obtención y validación de los registros de nacimiento relacionados a la Clave Única de Registro de Población (CURP) en el Registro Nacional de Población (RENAPO) localizados en México en formato JSON. Este endpoint no usa un algoritmo, sino que consulta las fuentes oficiales. Este servicio cumple con la normativa de nuestra parte, te recomendamos leer nuestros nuestros términos y condiciones.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[CurpAPIResponse]
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        from .curp_a_p_i_response400_error import CurpAPIResponse400Error
        from .curp_a_p_i_response401_error import CurpAPIResponse401Error
        from .curp_a_p_i_response404_error import CurpAPIResponse404Error
        from .curp_a_p_i_response4_x_x_error import CurpAPIResponse4XXError
        from .curp_a_p_i_response5_x_x_error import CurpAPIResponse5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": CurpAPIResponse400Error,
            "401": CurpAPIResponse401Error,
            "404": CurpAPIResponse404Error,
            "4XX": CurpAPIResponse4XXError,
            "5XX": CurpAPIResponse5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .....models.curp_a_p_i_response import CurpAPIResponse

        return await self.request_adapter.send_async(request_info, CurpAPIResponse, error_mapping)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration[ValidaCurpRequestBuilderPostQueryParameters]] = None) -> RequestInformation:
        """
        Valida CURP API, es una API REST para la obtención y validación de los registros de nacimiento relacionados a la Clave Única de Registro de Población (CURP) en el Registro Nacional de Población (RENAPO) localizados en México en formato JSON. Este endpoint no usa un algoritmo, sino que consulta las fuentes oficiales. Este servicio cumple con la normativa de nuestra parte, te recomendamos leer nuestros nuestros términos y condiciones.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> ValidaCurpRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: ValidaCurpRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return ValidaCurpRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class ValidaCurpRequestBuilderPostQueryParameters():
        """
        Valida CURP API, es una API REST para la obtención y validación de los registros de nacimiento relacionados a la Clave Única de Registro de Población (CURP) en el Registro Nacional de Población (RENAPO) localizados en México en formato JSON. Este endpoint no usa un algoritmo, sino que consulta las fuentes oficiales. Este servicio cumple con la normativa de nuestra parte, te recomendamos leer nuestros nuestros términos y condiciones.
        """
        # Clave Unica de Registro de Poblacion
        curp: Optional[str] = None

    
    @dataclass
    class ValidaCurpRequestBuilderPostRequestConfiguration(RequestConfiguration[ValidaCurpRequestBuilderPostQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

