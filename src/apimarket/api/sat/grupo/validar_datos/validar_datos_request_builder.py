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
    from .validar_datos400_error import ValidarDatos400Error
    from .validar_datos401_error import ValidarDatos401Error
    from .validar_datos404_error import ValidarDatos404Error
    from .validar_datos4_x_x_error import ValidarDatos4XXError
    from .validar_datos5_x_x_error import ValidarDatos5XXError
    from .validar_datos_post_response import ValidarDatosPostResponse

class ValidarDatosRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/sat/grupo/validar-datos
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new ValidarDatosRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/sat/grupo/validar-datos{?cp*,nombre*,regimen*,rfc*}", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration[ValidarDatosRequestBuilderPostQueryParameters]] = None) -> Optional[ValidarDatosPostResponse]:
        """
        Valida los datos enviados buscando coincidencia con los registros en la base de datos del **SAT.**_Nota: Si el usuario a consultar tiene mas de un regimen, separe los condigo con un_ "|"
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ValidarDatosPostResponse]
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        from .validar_datos400_error import ValidarDatos400Error
        from .validar_datos401_error import ValidarDatos401Error
        from .validar_datos404_error import ValidarDatos404Error
        from .validar_datos4_x_x_error import ValidarDatos4XXError
        from .validar_datos5_x_x_error import ValidarDatos5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": ValidarDatos400Error,
            "401": ValidarDatos401Error,
            "404": ValidarDatos404Error,
            "4XX": ValidarDatos4XXError,
            "5XX": ValidarDatos5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .validar_datos_post_response import ValidarDatosPostResponse

        return await self.request_adapter.send_async(request_info, ValidarDatosPostResponse, error_mapping)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration[ValidarDatosRequestBuilderPostQueryParameters]] = None) -> RequestInformation:
        """
        Valida los datos enviados buscando coincidencia con los registros en la base de datos del **SAT.**_Nota: Si el usuario a consultar tiene mas de un regimen, separe los condigo con un_ "|"
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> ValidarDatosRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: ValidarDatosRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return ValidarDatosRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class ValidarDatosRequestBuilderPostQueryParameters():
        """
        Valida los datos enviados buscando coincidencia con los registros en la base de datos del **SAT.**_Nota: Si el usuario a consultar tiene mas de un regimen, separe los condigo con un_ "|"
        """
        cp: Optional[int] = None

        nombre: Optional[str] = None

        regimen: Optional[str] = None

        rfc: Optional[str] = None

    
    @dataclass
    class ValidarDatosRequestBuilderPostRequestConfiguration(RequestConfiguration[ValidarDatosRequestBuilderPostQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

