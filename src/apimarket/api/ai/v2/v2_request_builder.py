from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .kie.kie_request_builder import KieRequestBuilder
    from .mrz.mrz_request_builder import MrzRequestBuilder
    from .universal_ocr.universal_ocr_request_builder import UniversalOcrRequestBuilder

class V2RequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/ai/v2
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new V2RequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/ai/v2", path_parameters)
    
    @property
    def kie(self) -> KieRequestBuilder:
        """
        The kie property
        """
        from .kie.kie_request_builder import KieRequestBuilder

        return KieRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def mrz(self) -> MrzRequestBuilder:
        """
        The mrz property
        """
        from .mrz.mrz_request_builder import MrzRequestBuilder

        return MrzRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def universal_ocr(self) -> UniversalOcrRequestBuilder:
        """
        The universalOcr property
        """
        from .universal_ocr.universal_ocr_request_builder import UniversalOcrRequestBuilder

        return UniversalOcrRequestBuilder(self.request_adapter, self.path_parameters)
    

