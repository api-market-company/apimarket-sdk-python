from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_abstractions.default_query_parameters import QueryParameters
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.method import Method
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.request_option import RequestOption
from kiota_abstractions.serialization import Parsable, ParsableFactory
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union
from warnings import warn

if TYPE_CHECKING:
    from .historial_laboral400_error import HistorialLaboral400Error
    from .historial_laboral401_error import HistorialLaboral401Error
    from .historial_laboral4_x_x_error import HistorialLaboral4XXError
    from .historial_laboral5_x_x_error import HistorialLaboral5XXError
    from .historial_laboral_post_response import HistorialLaboralPostResponse

class HistorialLaboralRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/imss/grupo/historial-laboral
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new HistorialLaboralRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/imss/grupo/historial-laboral?curp={curp}&nss={nss}", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration[HistorialLaboralRequestBuilderPostQueryParameters]] = None) -> Optional[HistorialLaboralPostResponse]:
        """
        Obtiene el historial Laboral registrado en el IMSS con sus semanas cotizadas, fechas de alta y baja, asi como el salario, razon social y registro patronal del empleador._Nota: Cada seguro social solo puede ser consultado 3 veces por dia, al exceder ese limite el sistema del seguro social bloquea las peticiones hasta pasar 24hrs._
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[HistorialLaboralPostResponse]
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        from .historial_laboral400_error import HistorialLaboral400Error
        from .historial_laboral401_error import HistorialLaboral401Error
        from .historial_laboral4_x_x_error import HistorialLaboral4XXError
        from .historial_laboral5_x_x_error import HistorialLaboral5XXError

        error_mapping: Dict[str, ParsableFactory] = {
            "400": HistorialLaboral400Error,
            "401": HistorialLaboral401Error,
            "4XX": HistorialLaboral4XXError,
            "5XX": HistorialLaboral5XXError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .historial_laboral_post_response import HistorialLaboralPostResponse

        return await self.request_adapter.send_async(request_info, HistorialLaboralPostResponse, error_mapping)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration[HistorialLaboralRequestBuilderPostQueryParameters]] = None) -> RequestInformation:
        """
        Obtiene el historial Laboral registrado en el IMSS con sus semanas cotizadas, fechas de alta y baja, asi como el salario, razon social y registro patronal del empleador._Nota: Cada seguro social solo puede ser consultado 3 veces por dia, al exceder ese limite el sistema del seguro social bloquea las peticiones hasta pasar 24hrs._
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> HistorialLaboralRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: HistorialLaboralRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return HistorialLaboralRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class HistorialLaboralRequestBuilderPostQueryParameters():
        """
        Obtiene el historial Laboral registrado en el IMSS con sus semanas cotizadas, fechas de alta y baja, asi como el salario, razon social y registro patronal del empleador._Nota: Cada seguro social solo puede ser consultado 3 veces por dia, al exceder ese limite el sistema del seguro social bloquea las peticiones hasta pasar 24hrs._
        """
        # Clave Unica de Registro de Poblacion
        curp: Optional[str] = None

        # Numero de Seguro Social
        nss: Optional[int] = None

    
    @dataclass
    class HistorialLaboralRequestBuilderPostRequestConfiguration(RequestConfiguration[HistorialLaboralRequestBuilderPostQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

