from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .obtener_cedula.obtener_cedula_request_builder import ObtenerCedulaRequestBuilder
    from .validar_cedula.validar_cedula_request_builder import ValidarCedulaRequestBuilder
    from .validar_certificado.validar_certificado_request_builder import ValidarCertificadoRequestBuilder

class GrupoRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/sep/grupo
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new GrupoRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/sep/grupo", path_parameters)
    
    @property
    def obtener_cedula(self) -> ObtenerCedulaRequestBuilder:
        """
        The obtenerCedula property
        """
        from .obtener_cedula.obtener_cedula_request_builder import ObtenerCedulaRequestBuilder

        return ObtenerCedulaRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def validar_cedula(self) -> ValidarCedulaRequestBuilder:
        """
        The validarCedula property
        """
        from .validar_cedula.validar_cedula_request_builder import ValidarCedulaRequestBuilder

        return ValidarCedulaRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def validar_certificado(self) -> ValidarCertificadoRequestBuilder:
        """
        The validarCertificado property
        """
        from .validar_certificado.validar_certificado_request_builder import ValidarCertificadoRequestBuilder

        return ValidarCertificadoRequestBuilder(self.request_adapter, self.path_parameters)
    

