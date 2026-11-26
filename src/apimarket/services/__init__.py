"""Servicios declarativos de API Market. Se reexportan desde :mod:`apimarket`."""
from apimarket.services import account, ai, government, imss, infonavit, sat
from apimarket.services._core import REGISTRY, ApiMarketError, FileInput, ServiceSpec

__all__ = ["ApiMarketError", "FileInput"] + [spec.function.__name__ for spec in REGISTRY]

globals().update({spec.function.__name__: spec.function for spec in REGISTRY})
