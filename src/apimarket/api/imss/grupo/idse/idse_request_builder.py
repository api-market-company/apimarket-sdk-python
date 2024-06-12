from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .capturar_movimientos_afiliatorios.capturar_movimientos_afiliatorios_request_builder import CapturarMovimientosAfiliatoriosRequestBuilder
    from .consultar_movimientos_afiliatorios.consultar_movimientos_afiliatorios_request_builder import ConsultarMovimientosAfiliatoriosRequestBuilder
    from .seguir_lote.seguir_lote_request_builder import SeguirLoteRequestBuilder

class IdseRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/imss/grupo/idse
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new IdseRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/imss/grupo/idse", path_parameters)
    
    @property
    def capturar_movimientos_afiliatorios(self) -> CapturarMovimientosAfiliatoriosRequestBuilder:
        """
        The capturarMovimientosAfiliatorios property
        """
        from .capturar_movimientos_afiliatorios.capturar_movimientos_afiliatorios_request_builder import CapturarMovimientosAfiliatoriosRequestBuilder

        return CapturarMovimientosAfiliatoriosRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def consultar_movimientos_afiliatorios(self) -> ConsultarMovimientosAfiliatoriosRequestBuilder:
        """
        The consultarMovimientosAfiliatorios property
        """
        from .consultar_movimientos_afiliatorios.consultar_movimientos_afiliatorios_request_builder import ConsultarMovimientosAfiliatoriosRequestBuilder

        return ConsultarMovimientosAfiliatoriosRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def seguir_lote(self) -> SeguirLoteRequestBuilder:
        """
        The seguirLote property
        """
        from .seguir_lote.seguir_lote_request_builder import SeguirLoteRequestBuilder

        return SeguirLoteRequestBuilder(self.request_adapter, self.path_parameters)
    

