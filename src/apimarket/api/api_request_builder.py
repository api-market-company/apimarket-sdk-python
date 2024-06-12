from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .ai.ai_request_builder import AiRequestBuilder
    from .balance.balance_request_builder import BalanceRequestBuilder
    from .imss.imss_request_builder import ImssRequestBuilder
    from .infonavit.infonavit_request_builder import InfonavitRequestBuilder
    from .renapo.renapo_request_builder import RenapoRequestBuilder
    from .sat.sat_request_builder import SatRequestBuilder
    from .sep.sep_request_builder import SepRequestBuilder
    from .v2.v2_request_builder import V2RequestBuilder

class ApiRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new ApiRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api", path_parameters)
    
    @property
    def ai(self) -> AiRequestBuilder:
        """
        The ai property
        """
        from .ai.ai_request_builder import AiRequestBuilder

        return AiRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def balance(self) -> BalanceRequestBuilder:
        """
        The balance property
        """
        from .balance.balance_request_builder import BalanceRequestBuilder

        return BalanceRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def imss(self) -> ImssRequestBuilder:
        """
        The imss property
        """
        from .imss.imss_request_builder import ImssRequestBuilder

        return ImssRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def infonavit(self) -> InfonavitRequestBuilder:
        """
        The infonavit property
        """
        from .infonavit.infonavit_request_builder import InfonavitRequestBuilder

        return InfonavitRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def renapo(self) -> RenapoRequestBuilder:
        """
        The renapo property
        """
        from .renapo.renapo_request_builder import RenapoRequestBuilder

        return RenapoRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def sat(self) -> SatRequestBuilder:
        """
        The sat property
        """
        from .sat.sat_request_builder import SatRequestBuilder

        return SatRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def sep(self) -> SepRequestBuilder:
        """
        The sep property
        """
        from .sep.sep_request_builder import SepRequestBuilder

        return SepRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def v2(self) -> V2RequestBuilder:
        """
        The v2 property
        """
        from .v2.v2_request_builder import V2RequestBuilder

        return V2RequestBuilder(self.request_adapter, self.path_parameters)
    

