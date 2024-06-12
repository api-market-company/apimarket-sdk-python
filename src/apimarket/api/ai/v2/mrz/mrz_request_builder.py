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
    from .mrz400_error import Mrz400Error
    from .mrz401_error import Mrz401Error
    from .mrz4_x_x_error import Mrz4XXError
    from .mrz5_x_x_error import Mrz5XXError
    from .mrz_post_request_body import MrzPostRequestBody
    from .mrz_post_response import MrzPostResponse

class MrzRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/ai/v2/mrz
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new MrzRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/ai/v2/mrz", path_parameters)
    
    async def post(self,body: MrzPostRequestBody, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[MrzPostResponse]:
        """
        Extraccion de datos en identificaciones internacionales como pasaportes, INE, Visas y otros que contienen una Zona de lectura mecánica (MRZ). Este endpoint tiene soporte para multiples paises y tipos de documentos le permitira procesar imágenes de documentos para encontrar y analizar el MRZ y la Zona de inspección visual (VIZ).
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[MrzPostResponse]
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        from .mrz400_error import Mrz400Error
        from .mrz401_error import Mrz401Error
        from .mrz4_x_x_error import Mrz4XXError
        from .mrz5_x_x_error import Mrz5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": Mrz400Error,
            "401": Mrz401Error,
            "4XX": Mrz4XXError,
            "5XX": Mrz5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .mrz_post_response import MrzPostResponse

        return await self.request_adapter.send_async(request_info, MrzPostResponse, error_mapping)
    
    def to_post_request_information(self,body: MrzPostRequestBody, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Extraccion de datos en identificaciones internacionales como pasaportes, INE, Visas y otros que contienen una Zona de lectura mecánica (MRZ). Este endpoint tiene soporte para multiples paises y tipos de documentos le permitira procesar imágenes de documentos para encontrar y analizar el MRZ y la Zona de inspección visual (VIZ).
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_parsable(self.request_adapter, "multipart/form-data", body)
        return request_info
    
    def with_url(self,raw_url: str) -> MrzRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: MrzRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return MrzRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class MrzRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

