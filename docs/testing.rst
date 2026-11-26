Testing
=======

El proyecto usa **pytest** con dos tipos de tests: unitarios y de integración.
Todos los tests corren dentro de Docker para garantizar un entorno consistente.

----

Tipos de tests
--------------

**Unitarios**
  No requieren conexión a ningún servicio externo. Verifican que las validaciones
  de datos se disparen correctamente antes de cualquier llamada a la API.
  Se pueden correr en cualquier momento sin configuración adicional.

**Integración** (marcados con ``@pytest.mark.integracion``)
  Llaman a las APIs reales. Requieren una API key válida configurada en el entorno.

----

Configuración
-------------

Crea un archivo ``.env`` en la raíz del proyecto con las variables necesarias:

.. code-block:: bash

    APIMARKET_API_KEY=tu_api_key_aqui

    # Solo requeridas para tests de IDSE Pro
    IDSEPRO_BEARER_TOKEN=tu_bearer_token
    IDSEPRO_API_KEY=tu_api_key_idse

Las pruebas de integración envían una CURP de prueba. Para usar otra sin guardarla en el repositorio:

.. code-block:: bash

    APIMARKET_TEST_CURP=tu_curp

Las pruebas que usan el fixture ``sdk`` consumen saldo salvo en modo sandbox. Las de ``sdk_sandbox`` siempre
usan sandbox.

Para correr en modo sandbox (sin consumir créditos reales):

.. code-block:: bash

    APIMARKET_SANDBOX=true

----

Ejecutar tests
--------------

**Solo unitarios** (sin API key, sin conexión):

.. code-block:: bash

    docker-compose run --rm sdk-app pytest -m "not integracion"

**Solo integración** (requiere API key):

.. code-block:: bash

    docker-compose run --rm sdk-app pytest -m integracion

**Todos los tests**:

.. code-block:: bash

    docker-compose run --rm sdk-app pytest

**Un archivo específico**:

.. code-block:: bash

    docker-compose run --rm sdk-app pytest tests/validations/test_curp.py

**Un test específico**:

.. code-block:: bash

    docker-compose run --rm sdk-app pytest tests/validations/test_curp.py::TestValidateCurp::test_valid_curp

----

Estructura de tests
-------------------

.. code-block:: text

    tests/
    ├── conftest.py              # fixtures compartidos (sdk, sdk_async, sdk_sandbox, server)
    ├── support.py               # servidor local y comprobaciones compartidas
    ├── cases.py                 # petición esperada de cada servicio
    ├── datos.py                 # datos de las pruebas de integración
    ├── services/
    │   ├── test_core.py         # errores, reintentos, archivos y concurrencia
    │   ├── test_catalog.py      # códigos de error y su catálogo
    │   ├── test_error_codes.py  # un caso real por cada código
    │   └── test_help.py         # ayuda de la CLI y sus ejemplos
    ├── validations/             # validaciones de CURP, RFC, NSS y fecha
    ├── ai/                      # cada área tiene su archivo test_<area>_servicios.py
    ├── cuenta/
    ├── geo/
    ├── imss/
    ├── infonavit/
    ├── renapo/
    ├── repuve/
    ├── sat/
    └── sep/

----

Ver los códigos de error
------------------------

Muestra qué produce el SDK en cada caso, sin red ni llave:

.. code-block:: bash

    python tests/ver_errores.py
    python tests/ver_errores.py reporte.md

----

Fixtures disponibles
--------------------

Definidos en ``tests/conftest.py`` y disponibles en todos los tests:

``server``
  Servidor HTTP local que registra las peticiones. Permite probar un servicio sin red ni llave real.

``sdk_sandbox``
  Configura llamadas síncronas en modo sandbox. Usar en las pruebas de integración de los servicios por grupo.

``sdk``
  Configura el SDK para llamadas síncronas. Usar en tests de integración normales.

  .. code-block:: python

      def test_algo(self, sdk):
          response = apimarket.fetch_curp_details("LOOA531113HTCPBN07")

``sdk_async``
  Configura el SDK para llamadas asíncronas. Usar junto con ``@pytest.mark.anyio``.

  .. code-block:: python

      @pytest.mark.anyio
      async def test_algo_async(sdk_async):
          response = await apimarket.fetch_curp_details("LOOA531113HTCPBN07")

----

Convenciones
------------

- Los tests unitarios no llevan markers; solo usan el fixture ``server`` cuando necesitan observar la petición.
- Los tests de integración siempre llevan ``@pytest.mark.integracion`` y el fixture ``sdk`` o ``sdk_sandbox``.
- Un servicio nuevo requiere su caso en ``tests/cases.py``; una prueba falla si falta.
- Cada parámetro requiere un dato inválido en ``tests/validations/test_every_parameter.py``.
- Un parámetro nuevo requiere su descripción y ejemplo en ``apimarket/cli_help.py``.
- Un código de error nuevo se agrega a ``apimarket/errors.py`` y a ``docs/error_catalog.rst``.
- Usar ``@pytest.mark.parametrize`` para colecciones de datos de prueba.
- Los datos de prueba (CURPs, NSS, RFC) son fijos y conocidos — nunca dinámicos.
