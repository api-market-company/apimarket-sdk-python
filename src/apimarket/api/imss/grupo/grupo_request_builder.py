from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .consultar_vigencia.consultar_vigencia_request_builder import ConsultarVigenciaRequestBuilder
    from .con_clinica.con_clinica_request_builder import ConClinicaRequestBuilder
    from .historial_laboral.historial_laboral_request_builder import HistorialLaboralRequestBuilder
    from .idse.idse_request_builder import IdseRequestBuilder
    from .localizar_nss.localizar_nss_request_builder import LocalizarNssRequestBuilder
    from .localizar_umf.localizar_umf_request_builder import LocalizarUmfRequestBuilder
    from .umf_asignada.umf_asignada_request_builder import UmfAsignadaRequestBuilder

class GrupoRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/imss/grupo
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new GrupoRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/imss/grupo", path_parameters)
    
    @property
    def con_clinica(self) -> ConClinicaRequestBuilder:
        """
        The conClinica property
        """
        from .con_clinica.con_clinica_request_builder import ConClinicaRequestBuilder

        return ConClinicaRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def consultar_vigencia(self) -> ConsultarVigenciaRequestBuilder:
        """
        The consultarVigencia property
        """
        from .consultar_vigencia.consultar_vigencia_request_builder import ConsultarVigenciaRequestBuilder

        return ConsultarVigenciaRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def historial_laboral(self) -> HistorialLaboralRequestBuilder:
        """
        The historialLaboral property
        """
        from .historial_laboral.historial_laboral_request_builder import HistorialLaboralRequestBuilder

        return HistorialLaboralRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def idse(self) -> IdseRequestBuilder:
        """
        The idse property
        """
        from .idse.idse_request_builder import IdseRequestBuilder

        return IdseRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def localizar_nss(self) -> LocalizarNssRequestBuilder:
        """
        The localizarNss property
        """
        from .localizar_nss.localizar_nss_request_builder import LocalizarNssRequestBuilder

        return LocalizarNssRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def localizar_umf(self) -> LocalizarUmfRequestBuilder:
        """
        The localizarUmf property
        """
        from .localizar_umf.localizar_umf_request_builder import LocalizarUmfRequestBuilder

        return LocalizarUmfRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def umf_asignada(self) -> UmfAsignadaRequestBuilder:
        """
        The umfAsignada property
        """
        from .umf_asignada.umf_asignada_request_builder import UmfAsignadaRequestBuilder

        return UmfAsignadaRequestBuilder(self.request_adapter, self.path_parameters)
    

