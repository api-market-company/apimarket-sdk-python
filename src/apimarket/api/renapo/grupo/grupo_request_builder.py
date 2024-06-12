from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .obtener_curp.obtener_curp_request_builder import ObtenerCurpRequestBuilder
    from .valida_curp.valida_curp_request_builder import ValidaCurpRequestBuilder

class GrupoRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/renapo/grupo
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new GrupoRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/renapo/grupo", path_parameters)
    
    @property
    def obtener_curp(self) -> ObtenerCurpRequestBuilder:
        """
        The obtenerCurp property
        """
        from .obtener_curp.obtener_curp_request_builder import ObtenerCurpRequestBuilder

        return ObtenerCurpRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def valida_curp(self) -> ValidaCurpRequestBuilder:
        """
        The validaCurp property
        """
        from .valida_curp.valida_curp_request_builder import ValidaCurpRequestBuilder

        return ValidaCurpRequestBuilder(self.request_adapter, self.path_parameters)
    

