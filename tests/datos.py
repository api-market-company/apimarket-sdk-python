"""Datos de las pruebas de integración."""
from decouple import config

#: CURP que se envía a la API real. Defina APIMARKET_TEST_CURP en .env para usar otra sin versionarla.
CURP_INTEGRACION = config("APIMARKET_TEST_CURP", default="XEXX010101MNEXXXA4")
