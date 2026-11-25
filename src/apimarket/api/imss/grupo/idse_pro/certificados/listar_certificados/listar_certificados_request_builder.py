from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_abstractions.default_query_parameters import QueryParameters
from kiota_abstractions.method import Method
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.serialization import ParsableFactory
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .listar_certificados400_error import ListarCertificados400Error
    from .listar_certificados401_error import ListarCertificados401Error
    from .listar_certificados5_x_x_error import ListarCertificados5XXError
    from .listar_certificados_get_response import Certificado


class ListarCertificadosRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under GET /certificates
    """
    def __init__(self, request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        super().__init__(request_adapter, "{+idsepro_base_url}/certificates", path_parameters)

    async def get(self, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[List[Certificado]]:
        """
        Lista los certificados disponibles en IDSE Pro.
        """
        request_info = self.to_get_request_information(request_configuration)
        from .listar_certificados400_error import ListarCertificados400Error
        from .listar_certificados401_error import ListarCertificados401Error
        from .listar_certificados5_x_x_error import ListarCertificados5XXError
        from .listar_certificados_get_response import Certificado
        error_mapping: Dict[str, ParsableFactory] = {
            "400": ListarCertificados400Error,
            "401": ListarCertificados401Error,
            "5XX": ListarCertificados5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null")
        return await self.request_adapter.send_collection_async(request_info, Certificado, error_mapping)

    def to_get_request_information(self, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info

    def with_url(self, raw_url: str) -> ListarCertificadosRequestBuilder:
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return ListarCertificadosRequestBuilder(self.request_adapter, raw_url)
