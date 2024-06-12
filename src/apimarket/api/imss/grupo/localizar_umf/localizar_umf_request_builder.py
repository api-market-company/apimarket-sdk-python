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
    from .localizar_umf400_error import LocalizarUmf400Error
    from .localizar_umf401_error import LocalizarUmf401Error
    from .localizar_umf4_x_x_error import LocalizarUmf4XXError
    from .localizar_umf5_x_x_error import LocalizarUmf5XXError
    from .localizar_umf_post_response import LocalizarUmfPostResponse

class LocalizarUmfRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/imss/grupo/localizar-umf
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new LocalizarUmfRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/imss/grupo/localizar-umf?cp={cp}", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration[LocalizarUmfRequestBuilderPostQueryParameters]] = None) -> Optional[LocalizarUmfPostResponse]:
        """
        Obtiene las clinicas que brindan atencion medica a los habitantes de ese codigo postal, las clinicas mas cercanas y posibles asignadas, brinda coordenadas de ubicacion, direccion y numero de contacto de cada clinica.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[LocalizarUmfPostResponse]
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        from .localizar_umf400_error import LocalizarUmf400Error
        from .localizar_umf401_error import LocalizarUmf401Error
        from .localizar_umf4_x_x_error import LocalizarUmf4XXError
        from .localizar_umf5_x_x_error import LocalizarUmf5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": LocalizarUmf400Error,
            "401": LocalizarUmf401Error,
            "4XX": LocalizarUmf4XXError,
            "5XX": LocalizarUmf5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .localizar_umf_post_response import LocalizarUmfPostResponse

        return await self.request_adapter.send_async(request_info, LocalizarUmfPostResponse, error_mapping)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration[LocalizarUmfRequestBuilderPostQueryParameters]] = None) -> RequestInformation:
        """
        Obtiene las clinicas que brindan atencion medica a los habitantes de ese codigo postal, las clinicas mas cercanas y posibles asignadas, brinda coordenadas de ubicacion, direccion y numero de contacto de cada clinica.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> LocalizarUmfRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: LocalizarUmfRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return LocalizarUmfRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class LocalizarUmfRequestBuilderPostQueryParameters():
        """
        Obtiene las clinicas que brindan atencion medica a los habitantes de ese codigo postal, las clinicas mas cercanas y posibles asignadas, brinda coordenadas de ubicacion, direccion y numero de contacto de cada clinica.
        """
        # Codigo Postal
        cp: Optional[int] = None

    
    @dataclass
    class LocalizarUmfRequestBuilderPostRequestConfiguration(RequestConfiguration[LocalizarUmfRequestBuilderPostQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

