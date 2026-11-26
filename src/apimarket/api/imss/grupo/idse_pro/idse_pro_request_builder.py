from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Dict, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .certificados.certificados_request_builder import CertificadosRequestBuilder


class IdseProRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under https://idsepro.apimarket.mx/rest/v1
    """
    def __init__(self, request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        super().__init__(request_adapter, "{+idsepro_base_url}", path_parameters)

    @property
    def certificados(self) -> CertificadosRequestBuilder:
        from .certificados.certificados_request_builder import CertificadosRequestBuilder
        return CertificadosRequestBuilder(self.request_adapter, self.path_parameters)
