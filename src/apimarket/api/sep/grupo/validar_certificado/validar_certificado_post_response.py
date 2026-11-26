from __future__ import annotations
import warnings

from apimarket.api.sep.grupo.validar_certificado.validar_certificado_get_response import ValidarCertificadoGetResponse


def __getattr__(name: str):
    if name == "ValidarCertificadoPostResponse":
        warnings.warn(
            "ValidarCertificadoPostResponse fue renombrado a ValidarCertificadoGetResponse. "
            "Actualice su import: "
            "from apimarket.api.sep.grupo.validar_certificado.validar_certificado_get_response "
            "import ValidarCertificadoGetResponse",
            DeprecationWarning,
            stacklevel=2,
        )
        return ValidarCertificadoGetResponse
    raise AttributeError(f"El módulo 'validar_certificado_post_response' no tiene el atributo {name!r}")
