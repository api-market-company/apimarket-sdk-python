from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .permissions.permissions_request_builder import PermissionsRequestBuilder
    from .public_key.public_key_request_builder import PublicKeyRequestBuilder
    from .tokens.tokens_request_builder import TokensRequestBuilder

class ApimarketRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/v2/apimarket
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new ApimarketRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/v2/apimarket", path_parameters)
    
    @property
    def permissions(self) -> PermissionsRequestBuilder:
        """
        The permissions property
        """
        from .permissions.permissions_request_builder import PermissionsRequestBuilder

        return PermissionsRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def public_key(self) -> PublicKeyRequestBuilder:
        """
        The publicKey property
        """
        from .public_key.public_key_request_builder import PublicKeyRequestBuilder

        return PublicKeyRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def tokens(self) -> TokensRequestBuilder:
        """
        The tokens property
        """
        from .tokens.tokens_request_builder import TokensRequestBuilder

        return TokensRequestBuilder(self.request_adapter, self.path_parameters)
    

