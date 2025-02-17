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
    from .lista69b400_error import Lista69b400Error
    from .lista69b401_error import Lista69b401Error
    from .lista69b4_x_x_error import Lista69b4XXError
    from .lista69b5_x_x_error import Lista69b5XXError
    from .lista69b_post_response import Lista69bPostResponse

class Lista69bRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/sat/v2/lista69b
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new Lista69bRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/sat/v2/lista69b{?contribuyente*,rfc*,select*}", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration[Lista69bRequestBuilderPostQueryParameters]] = None) -> Optional[Lista69bPostResponse]:
        """
        Consulta la lista 69B del SAT (Lista negra) con distintos filtros horizontales y verticales.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[Lista69bPostResponse]
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        from .lista69b400_error import Lista69b400Error
        from .lista69b401_error import Lista69b401Error
        from .lista69b4_x_x_error import Lista69b4XXError
        from .lista69b5_x_x_error import Lista69b5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": Lista69b400Error,
            "401": Lista69b401Error,
            "4XX": Lista69b4XXError,
            "5XX": Lista69b5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .lista69b_post_response import Lista69bPostResponse

        return await self.request_adapter.send_async(request_info, Lista69bPostResponse, error_mapping)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration[Lista69bRequestBuilderPostQueryParameters]] = None) -> RequestInformation:
        """
        Consulta la lista 69B del SAT (Lista negra) con distintos filtros horizontales y verticales.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> Lista69bRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: Lista69bRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return Lista69bRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class Lista69bRequestBuilderPostQueryParameters():
        """
        Consulta la lista 69B del SAT (Lista negra) con distintos filtros horizontales y verticales.
        """
        # Con wfts buscas con un lenguaje cercano al natural. 
        contribuyente: Optional[str] = None

        # Con match buscas con un expresión regular POSIX.
        rfc: Optional[str] = None

        # Campos que quieres mostrar. Recuerda que menor cantidad de campos, menor es el tiempo de espera.
        select: Optional[str] = None

    
    @dataclass
    class Lista69bRequestBuilderPostRequestConfiguration(RequestConfiguration[Lista69bRequestBuilderPostQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

