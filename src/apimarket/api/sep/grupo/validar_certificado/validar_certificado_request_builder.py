from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.method import Method
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.serialization import Parsable, ParsableFactory
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .validar_certificado400_error import ValidarCertificado400Error
    from .validar_certificado401_error import ValidarCertificado401Error
    from .validar_certificado404_error import ValidarCertificado404Error
    from .validar_certificado4_x_x_error import ValidarCertificado4XXError
    from .validar_certificado5_x_x_error import ValidarCertificado5XXError
    from .validar_certificado_get_response import ValidarCertificadoGetResponse

class ValidarCertificadoRequestBuilder(BaseRequestBuilder):
    def __init__(self, request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        super().__init__(request_adapter, "{+baseurl}/api/sep/grupo/validar-certificado?folio={folio}", path_parameters)

    async def post(self, request_configuration: Optional[RequestConfiguration] = None) -> Optional[ValidarCertificadoGetResponse]:
        request_info = self.to_post_request_information(request_configuration)
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
        from .validar_certificado_get_response import ValidarCertificadoGetResponse
        return await self.request_adapter.send_async(request_info, ValidarCertificadoGetResponse, error_mapping)

    def to_post_request_information(self, request_configuration: Optional[RequestConfiguration] = None) -> RequestInformation:
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info

    def with_url(self, raw_url: str) -> ValidarCertificadoRequestBuilder:
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return ValidarCertificadoRequestBuilder(self.request_adapter, raw_url)

    @dataclass
    class ValidarCertificadoRequestBuilderPostQueryParameters():
        folio: Optional[str] = None
