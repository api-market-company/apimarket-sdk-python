from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Dict, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .listar_certificados.listar_certificados_request_builder import ListarCertificadosRequestBuilder


class CertificadosRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /certificates
    """
    def __init__(self, request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        super().__init__(request_adapter, "{+idsepro_base_url}/certificates", path_parameters)

    @property
    def listar_certificados(self) -> ListarCertificadosRequestBuilder:
        from .listar_certificados.listar_certificados_request_builder import ListarCertificadosRequestBuilder
        return ListarCertificadosRequestBuilder(self.request_adapter, self.path_parameters)
