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
    from .codigos_postales import CodigosPostales
    from .codigos_postales400_error import CodigosPostales400Error
    from .codigos_postales401_error import CodigosPostales401Error
    from .codigos_postales4_x_x_error import CodigosPostales4XXError
    from .codigos_postales5_x_x_error import CodigosPostales5XXError

class CodigosPostalesRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/v2/codigos-postales
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new CodigosPostalesRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/v2/codigos-postales{?country_code*,postal_code*,postal_code_mx*,select*}", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration[CodigosPostalesRequestBuilderPostQueryParameters]] = None) -> Optional[List[CodigosPostales]]:
        """
        Accede a información detallada de códigos postales en todo México y de otros países utilizando filtros avanzados. El servicio devuelve datos en el formato especificado, que incluye campos como id, código de país, código postal, nombre del lugar, nombres y códigos administrativos, y fecha de actualización.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[List[CodigosPostales]]
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        from .codigos_postales400_error import CodigosPostales400Error
        from .codigos_postales401_error import CodigosPostales401Error
        from .codigos_postales4_x_x_error import CodigosPostales4XXError
        from .codigos_postales5_x_x_error import CodigosPostales5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": CodigosPostales400Error,
            "401": CodigosPostales401Error,
            "4XX": CodigosPostales4XXError,
            "5XX": CodigosPostales5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .codigos_postales import CodigosPostales

        return await self.request_adapter.send_collection_async(request_info, CodigosPostales, error_mapping)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration[CodigosPostalesRequestBuilderPostQueryParameters]] = None) -> RequestInformation:
        """
        Accede a información detallada de códigos postales en todo México y de otros países utilizando filtros avanzados. El servicio devuelve datos en el formato especificado, que incluye campos como id, código de país, código postal, nombre del lugar, nombres y códigos administrativos, y fecha de actualización.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> CodigosPostalesRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: CodigosPostalesRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return CodigosPostalesRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class CodigosPostalesRequestBuilderPostQueryParameters():
        """
        Accede a información detallada de códigos postales en todo México y de otros países utilizando filtros avanzados. El servicio devuelve datos en el formato especificado, que incluye campos como id, código de país, código postal, nombre del lugar, nombres y códigos administrativos, y fecha de actualización.
        """
        # Código del país según ISO. Puedes utilizar operadores para filtros avanzados.
        country_code: Optional[str] = None

        # Ingresa el código postal que deseas consultar.
        postal_code: Optional[str] = None

        # Ingresa el código postal que deseas consultar de México.
        postal_code_mx: Optional[str] = None

        # Campos que deseas mostrar en la respuesta. Menos campos seleccionados resultan en una respuesta más rápida. Usa el parámetro 'select' de PostgREST.
        select: Optional[str] = None

    
    @dataclass
    class CodigosPostalesRequestBuilderPostRequestConfiguration(RequestConfiguration[CodigosPostalesRequestBuilderPostQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

