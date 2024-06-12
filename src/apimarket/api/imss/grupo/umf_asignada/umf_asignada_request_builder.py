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
    from .umf_asignada400_error import UmfAsignada400Error
    from .umf_asignada401_error import UmfAsignada401Error
    from .umf_asignada4_x_x_error import UmfAsignada4XXError
    from .umf_asignada5_x_x_error import UmfAsignada5XXError
    from .umf_asignada_post_response import UmfAsignadaPostResponse

class UmfAsignadaRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/imss/grupo/umf-asignada
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new UmfAsignadaRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/imss/grupo/umf-asignada?nss={nss}", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration[UmfAsignadaRequestBuilderPostQueryParameters]] = None) -> Optional[UmfAsignadaPostResponse]:
        """
        Obten la Unidad Medico Familiar asignada por el Instituto Mexicano del Seguro Social (IMSS) a tus usuarios.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[UmfAsignadaPostResponse]
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        from .umf_asignada400_error import UmfAsignada400Error
        from .umf_asignada401_error import UmfAsignada401Error
        from .umf_asignada4_x_x_error import UmfAsignada4XXError
        from .umf_asignada5_x_x_error import UmfAsignada5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": UmfAsignada400Error,
            "401": UmfAsignada401Error,
            "4XX": UmfAsignada4XXError,
            "5XX": UmfAsignada5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .umf_asignada_post_response import UmfAsignadaPostResponse

        return await self.request_adapter.send_async(request_info, UmfAsignadaPostResponse, error_mapping)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration[UmfAsignadaRequestBuilderPostQueryParameters]] = None) -> RequestInformation:
        """
        Obten la Unidad Medico Familiar asignada por el Instituto Mexicano del Seguro Social (IMSS) a tus usuarios.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> UmfAsignadaRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: UmfAsignadaRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return UmfAsignadaRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class UmfAsignadaRequestBuilderPostQueryParameters():
        """
        Obten la Unidad Medico Familiar asignada por el Instituto Mexicano del Seguro Social (IMSS) a tus usuarios.
        """
        # Numero de Seguro Social
        nss: Optional[int] = None

    
    @dataclass
    class UmfAsignadaRequestBuilderPostRequestConfiguration(RequestConfiguration[UmfAsignadaRequestBuilderPostQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

