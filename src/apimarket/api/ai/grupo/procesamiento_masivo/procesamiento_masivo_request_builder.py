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
    from .procesamiento_masivo400_error import ProcesamientoMasivo400Error
    from .procesamiento_masivo401_error import ProcesamientoMasivo401Error
    from .procesamiento_masivo4_x_x_error import ProcesamientoMasivo4XXError
    from .procesamiento_masivo5_x_x_error import ProcesamientoMasivo5XXError
    from .procesamiento_masivo_post_request_body import ProcesamientoMasivoPostRequestBody

class ProcesamientoMasivoRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/ai/grupo/procesamiento-masivo
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new ProcesamientoMasivoRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/ai/grupo/procesamiento-masivo", path_parameters)
    
    async def post(self,body: ProcesamientoMasivoPostRequestBody, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[List[str]]:
        """
        Procesa los archivos, bases de datos y webs que necesites, integra de manera fluida servicios tanto de API Market como externos, escala con nuestro clúster, elimina el ruido de los rate limit y proxies.
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[List[str]]
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        from .procesamiento_masivo400_error import ProcesamientoMasivo400Error
        from .procesamiento_masivo401_error import ProcesamientoMasivo401Error
        from .procesamiento_masivo4_x_x_error import ProcesamientoMasivo4XXError
        from .procesamiento_masivo5_x_x_error import ProcesamientoMasivo5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": ProcesamientoMasivo400Error,
            "401": ProcesamientoMasivo401Error,
            "4XX": ProcesamientoMasivo4XXError,
            "5XX": ProcesamientoMasivo5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_collection_of_primitive_async(request_info, "str", error_mapping)
    
    def to_post_request_information(self,body: ProcesamientoMasivoPostRequestBody, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Procesa los archivos, bases de datos y webs que necesites, integra de manera fluida servicios tanto de API Market como externos, escala con nuestro clúster, elimina el ruido de los rate limit y proxies.
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_parsable(self.request_adapter, "application/json", body)
        return request_info
    
    def with_url(self,raw_url: str) -> ProcesamientoMasivoRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: ProcesamientoMasivoRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return ProcesamientoMasivoRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class ProcesamientoMasivoRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

