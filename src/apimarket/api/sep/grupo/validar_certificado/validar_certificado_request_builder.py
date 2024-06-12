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
    from .validar_certificado400_error import ValidarCertificado400Error
    from .validar_certificado401_error import ValidarCertificado401Error
    from .validar_certificado404_error import ValidarCertificado404Error
    from .validar_certificado4_x_x_error import ValidarCertificado4XXError
    from .validar_certificado5_x_x_error import ValidarCertificado5XXError
    from .validar_certificado_post_response import ValidarCertificadoPostResponse

class ValidarCertificadoRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/sep/grupo/validar-certificado
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new ValidarCertificadoRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/sep/grupo/validar-certificado{?folio*}", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration[ValidarCertificadoRequestBuilderPostQueryParameters]] = None) -> Optional[ValidarCertificadoPostResponse]:
        """
        Busqueda de folio electronico de certificados en el sistema DGETI de la Secretaria de Educacion Publica._Nota: Solo podran ser consultados los certificados que se encuentren Digitalizados (Que tengan QR)_
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ValidarCertificadoPostResponse]
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        from .validar_certificado400_error import ValidarCertificado400Error
        from .validar_certificado401_error import ValidarCertificado401Error
        from .validar_certificado404_error import ValidarCertificado404Error
        from .validar_certificado4_x_x_error import ValidarCertificado4XXError
        from .validar_certificado5_x_x_error import ValidarCertificado5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": ValidarCertificado400Error,
            "401": ValidarCertificado401Error,
            "404": ValidarCertificado404Error,
            "4XX": ValidarCertificado4XXError,
            "5XX": ValidarCertificado5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .validar_certificado_post_response import ValidarCertificadoPostResponse

        return await self.request_adapter.send_async(request_info, ValidarCertificadoPostResponse, error_mapping)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration[ValidarCertificadoRequestBuilderPostQueryParameters]] = None) -> RequestInformation:
        """
        Busqueda de folio electronico de certificados en el sistema DGETI de la Secretaria de Educacion Publica._Nota: Solo podran ser consultados los certificados que se encuentren Digitalizados (Que tengan QR)_
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> ValidarCertificadoRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: ValidarCertificadoRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return ValidarCertificadoRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class ValidarCertificadoRequestBuilderPostQueryParameters():
        """
        Busqueda de folio electronico de certificados en el sistema DGETI de la Secretaria de Educacion Publica._Nota: Solo podran ser consultados los certificados que se encuentren Digitalizados (Que tengan QR)_
        """
        # Folio Electronico del certificado
        folio: Optional[str] = None

    
    @dataclass
    class ValidarCertificadoRequestBuilderPostRequestConfiguration(RequestConfiguration[ValidarCertificadoRequestBuilderPostQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

