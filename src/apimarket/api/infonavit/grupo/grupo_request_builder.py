from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .buscar_credito.buscar_credito_request_builder import BuscarCreditoRequestBuilder
    from .obtener_cuenta.obtener_cuenta_request_builder import ObtenerCuentaRequestBuilder

class GrupoRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/infonavit/grupo
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new GrupoRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/infonavit/grupo", path_parameters)
    
    @property
    def buscar_credito(self) -> BuscarCreditoRequestBuilder:
        """
        The buscarCredito property
        """
        from .buscar_credito.buscar_credito_request_builder import BuscarCreditoRequestBuilder

        return BuscarCreditoRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def obtener_cuenta(self) -> ObtenerCuentaRequestBuilder:
        """
        The obtenerCuenta property
        """
        from .obtener_cuenta.obtener_cuenta_request_builder import ObtenerCuentaRequestBuilder

        return ObtenerCuentaRequestBuilder(self.request_adapter, self.path_parameters)
    

