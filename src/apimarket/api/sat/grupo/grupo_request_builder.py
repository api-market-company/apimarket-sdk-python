from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .calcular_rfc.calcular_rfc_request_builder import CalcularRfcRequestBuilder
    from .obtener_datos.obtener_datos_request_builder import ObtenerDatosRequestBuilder
    from .obtener_datos_idcif.obtener_datos_idcif_request_builder import ObtenerDatosIdcifRequestBuilder
    from .obtener_rfc.obtener_rfc_request_builder import ObtenerRfcRequestBuilder
    from .validar_datos.validar_datos_request_builder import ValidarDatosRequestBuilder
    from .verificar_firma_electronica.verificar_firma_electronica_request_builder import VerificarFirmaElectronicaRequestBuilder

class GrupoRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/sat/grupo
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new GrupoRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/sat/grupo", path_parameters)
    
    @property
    def calcular_rfc(self) -> CalcularRfcRequestBuilder:
        """
        The calcularRfc property
        """
        from .calcular_rfc.calcular_rfc_request_builder import CalcularRfcRequestBuilder

        return CalcularRfcRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def obtener_datos(self) -> ObtenerDatosRequestBuilder:
        """
        The obtenerDatos property
        """
        from .obtener_datos.obtener_datos_request_builder import ObtenerDatosRequestBuilder

        return ObtenerDatosRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def obtener_datos_idcif(self) -> ObtenerDatosIdcifRequestBuilder:
        """
        The obtenerDatosIdcif property
        """
        from .obtener_datos_idcif.obtener_datos_idcif_request_builder import ObtenerDatosIdcifRequestBuilder

        return ObtenerDatosIdcifRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def obtener_rfc(self) -> ObtenerRfcRequestBuilder:
        """
        The obtenerRfc property
        """
        from .obtener_rfc.obtener_rfc_request_builder import ObtenerRfcRequestBuilder

        return ObtenerRfcRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def validar_datos(self) -> ValidarDatosRequestBuilder:
        """
        The validarDatos property
        """
        from .validar_datos.validar_datos_request_builder import ValidarDatosRequestBuilder

        return ValidarDatosRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def verificar_firma_electronica(self) -> VerificarFirmaElectronicaRequestBuilder:
        """
        The verificarFirmaElectronica property
        """
        from .verificar_firma_electronica.verificar_firma_electronica_request_builder import VerificarFirmaElectronicaRequestBuilder

        return VerificarFirmaElectronicaRequestBuilder(self.request_adapter, self.path_parameters)
    

