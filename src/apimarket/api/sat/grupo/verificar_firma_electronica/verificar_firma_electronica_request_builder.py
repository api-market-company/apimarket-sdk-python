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
    from .verificar_firma_electronica400_error import VerificarFirmaElectronica400Error
    from .verificar_firma_electronica401_error import VerificarFirmaElectronica401Error
    from .verificar_firma_electronica4_x_x_error import VerificarFirmaElectronica4XXError
    from .verificar_firma_electronica5_x_x_error import VerificarFirmaElectronica5XXError
    from .verificar_firma_electronica_post_request_body import VerificarFirmaElectronicaPostRequestBody
    from .verificar_firma_electronica_post_response import VerificarFirmaElectronicaPostResponse

class VerificarFirmaElectronicaRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/sat/grupo/verificar-firma-electronica
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new VerificarFirmaElectronicaRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/sat/grupo/verificar-firma-electronica", path_parameters)
    
    async def post(self,body: VerificarFirmaElectronicaPostRequestBody, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[VerificarFirmaElectronicaPostResponse]:
        """
        Verifica la firma electrónica de una persona física o moral; de manera criptográfica,realiza la validación de las credenciales y verifica con la Autoridad de Certificación (CA), en este caso, con el SAT,si ha expirado o ha dejado de representar al usuario.
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[VerificarFirmaElectronicaPostResponse]
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        from .verificar_firma_electronica400_error import VerificarFirmaElectronica400Error
        from .verificar_firma_electronica401_error import VerificarFirmaElectronica401Error
        from .verificar_firma_electronica4_x_x_error import VerificarFirmaElectronica4XXError
        from .verificar_firma_electronica5_x_x_error import VerificarFirmaElectronica5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": VerificarFirmaElectronica400Error,
            "401": VerificarFirmaElectronica401Error,
            "4XX": VerificarFirmaElectronica4XXError,
            "5XX": VerificarFirmaElectronica5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .verificar_firma_electronica_post_response import VerificarFirmaElectronicaPostResponse

        return await self.request_adapter.send_async(request_info, VerificarFirmaElectronicaPostResponse, error_mapping)
    
    def to_post_request_information(self,body: VerificarFirmaElectronicaPostRequestBody, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Verifica la firma electrónica de una persona física o moral; de manera criptográfica,realiza la validación de las credenciales y verifica con la Autoridad de Certificación (CA), en este caso, con el SAT,si ha expirado o ha dejado de representar al usuario.
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
    
    def with_url(self,raw_url: str) -> VerificarFirmaElectronicaRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: VerificarFirmaElectronicaRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return VerificarFirmaElectronicaRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class VerificarFirmaElectronicaRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

