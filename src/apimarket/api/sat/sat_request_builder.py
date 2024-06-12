from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .grupo.grupo_request_builder import GrupoRequestBuilder
    from .v2.v2_request_builder import V2RequestBuilder

class SatRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/sat
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new SatRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/sat", path_parameters)
    
    @property
    def grupo(self) -> GrupoRequestBuilder:
        """
        The grupo property
        """
        from .grupo.grupo_request_builder import GrupoRequestBuilder

        return GrupoRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def v2(self) -> V2RequestBuilder:
        """
        The v2 property
        """
        from .v2.v2_request_builder import V2RequestBuilder

        return V2RequestBuilder(self.request_adapter, self.path_parameters)
    

