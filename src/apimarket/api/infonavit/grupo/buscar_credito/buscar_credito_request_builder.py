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
    from .buscar_credito400_error import BuscarCredito400Error
    from .buscar_credito401_error import BuscarCredito401Error
    from .buscar_credito404_error import BuscarCredito404Error
    from .buscar_credito422_error import BuscarCredito422Error
    from .buscar_credito4_x_x_error import BuscarCredito4XXError
    from .buscar_credito5_x_x_error import BuscarCredito5XXError
    from .buscar_credito_post_response import BuscarCreditoPostResponse

class BuscarCreditoRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/infonavit/grupo/buscar-credito
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new BuscarCreditoRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/infonavit/grupo/buscar-credito?nss={nss}", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration[BuscarCreditoRequestBuilderPostQueryParameters]] = None) -> Optional[BuscarCreditoPostResponse]:
        """
        Endpoint para realizar la consulta de creditos en el infonavit, obtenida mediante el Numero de seguro social de la persona.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[BuscarCreditoPostResponse]
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        from .buscar_credito400_error import BuscarCredito400Error
        from .buscar_credito401_error import BuscarCredito401Error
        from .buscar_credito404_error import BuscarCredito404Error
        from .buscar_credito422_error import BuscarCredito422Error
        from .buscar_credito4_x_x_error import BuscarCredito4XXError
        from .buscar_credito5_x_x_error import BuscarCredito5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": BuscarCredito400Error,
            "401": BuscarCredito401Error,
            "404": BuscarCredito404Error,
            "422": BuscarCredito422Error,
            "4XX": BuscarCredito4XXError,
            "5XX": BuscarCredito5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .buscar_credito_post_response import BuscarCreditoPostResponse

        return await self.request_adapter.send_async(request_info, BuscarCreditoPostResponse, error_mapping)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration[BuscarCreditoRequestBuilderPostQueryParameters]] = None) -> RequestInformation:
        """
        Endpoint para realizar la consulta de creditos en el infonavit, obtenida mediante el Numero de seguro social de la persona.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> BuscarCreditoRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: BuscarCreditoRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return BuscarCreditoRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class BuscarCreditoRequestBuilderPostQueryParameters():
        """
        Endpoint para realizar la consulta de creditos en el infonavit, obtenida mediante el Numero de seguro social de la persona.
        """
        # Número de Seguro Social
        nss: Optional[int] = None

    
    @dataclass
    class BuscarCreditoRequestBuilderPostRequestConfiguration(RequestConfiguration[BuscarCreditoRequestBuilderPostQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

