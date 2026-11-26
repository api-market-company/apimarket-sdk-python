CLI Reference
=============

Referencia completa de todos los comandos disponibles en el CLI de API Market.

Uso general::

    apimarket [GRUPO] [OPCIONES]

La ayuda está en tres niveles; cada comando muestra parámetros, un ejemplo y sus códigos de error::

    apimarket -h                          # todos los comandos por área
    apimarket sat -h                      # los servicios de un área
    apimarket sat declaraciones -h        # un servicio
    apimarket errores curp                # códigos que contienen "curp"

Para ver la versión instalada::

    apimarket --version

----

RENAPO
------

**-vc / --validate-curp** ``CURP``

Valida un CURP contra el padrón de RENAPO y retorna los datos personales registrados.

.. code-block:: bash

    apimarket -vc LOOA531113HTCPBN07

----

**-cc / --calculate-curp** ``NOMBRES PATERNO MATERNO DIA MES AÑO ENTIDAD SEXO``

Obtiene el CURP a partir de datos personales.

.. code-block:: bash

    apimarket -cc "JUAN CARLOS" GARCIA MARTINEZ 15 03 1990 09 H

Valores válidos para ``SEXO``: ``H`` (hombre), ``M`` (mujer), ``X`` (no binario).

Valores válidos para ``ENTIDAD``: clave de 2 dígitos del estado de nacimiento (ej. ``09`` para CDMX).

----

SAT
---

**-ro / --get-rfc** ``CURP``

Obtiene el RFC a partir de un CURP.

.. code-block:: bash

    apimarket -ro LOOA531113HTCPBN07

----

**-cr / --calculate-rfc** ``NOMBRES PATERNO MATERNO DIA MES AÑO``

Calcula el RFC a partir de datos personales.

.. code-block:: bash

    apimarket -cr "JUAN CARLOS" GARCIA LOPEZ 01 01 1990

----

**-vs / --validate-sat** ``NOMBRE RFC REGIMEN CP``

Valida datos fiscales en el SAT.

.. code-block:: bash

    apimarket -vs "NOMBRE COMPLETO" GOAJ900101AB1 601 06600

----

**-df / --fiscal-data** ``RFC``

Obtiene datos fiscales registrados en el SAT por RFC.

.. code-block:: bash

    apimarket -df GOAJ900101AB1

----

IMSS
----

**-lu / --locate-umf** ``CP``

Localiza la UMF (Unidad de Medicina Familiar) correspondiente a un código postal.

.. code-block:: bash

    apimarket -lu 06600

----

**-ln / --locate-nss** ``CURP``

Localiza el NSS (Número de Seguridad Social) a partir de un CURP.

.. code-block:: bash

    apimarket -ln LOOA531113HTCPBN07

----

**-vi / --check-validity** ``NSS CURP``

Verifica la vigencia de derechos IMSS con NSS y CURP.

.. code-block:: bash

    apimarket -vi 12345678952 LOOA531113HTCPBN07

----

**-cl / --get-clinic** ``CURP``

Obtiene la clínica IMSS asignada a partir de un CURP.

.. code-block:: bash

    apimarket -cl LOOA531113HTCPBN07

----

**-hl / --labor-history** ``CURP NSS``

Consulta el historial laboral registrado en el IMSS.

.. code-block:: bash

    apimarket -hl LOOA531113HTCPBN07 12345678952

----

SEP
---

**-ce / --validate-cedula** ``CEDULA``

Valida una cédula profesional en la SEP.

.. code-block:: bash

    apimarket -ce 1234567

----

**-vr / --validate-certificate** ``FOLIO``

Valida un certificado de estudios por folio.

.. code-block:: bash

    apimarket -vr FOLIO123

----

**-oc / --get-cedula** ``NOMBRES PATERNO MATERNO``

Busca cédulas profesionales por datos personales.

.. code-block:: bash

    apimarket -oc "JUAN CARLOS" GARCIA MARTINEZ

----

INFONAVIT
---------

**-bc / --search-credit** ``NSS``

Busca crédito INFONAVIT asociado a un NSS.

.. code-block:: bash

    apimarket -bc 12345678952

----

**-si / --infonavit-subaccount** ``NSS``

Obtiene el saldo de la subcuenta de vivienda INFONAVIT.

.. code-block:: bash

    apimarket -si 12345678952

----

IDSE Pro
--------

**-lc / --list-certificates**

Lista los certificados digitales disponibles en IDSE Pro.
Requiere ``IDSEPRO_BEARER_TOKEN`` e ``IDSEPRO_API_KEY`` configurados.

.. code-block:: bash

    apimarket -lc

----

Cuenta
------

**-pm / --permissions**

Muestra los permisos asociados a la cuenta y API key activa.

.. code-block:: bash

    apimarket -pm

----

**-gt / --store-token** ``NOMBRE EMPRESA DESCRIPCION PERMISOS RFC CIEC``

Crea y guarda un nuevo token en la cuenta. ``PERMISOS`` es una lista separada por comas.

.. code-block:: bash

    apimarket -gt "Mi Token" "Mi Empresa" "Descripcion" "permiso1,permiso2" GOAJ900101AB1 ciec123

----

Servicios por grupo
-------------------

Además de las opciones anteriores, la CLI ofrece estos servicios::

    apimarket GRUPO SERVICIO [--parametro valor ...]

Para listarlos, ver los parámetros de uno o usar el modo de pruebas:

.. code-block:: bash

    apimarket servicios
    apimarket sat declaraciones --help
    apimarket repuve vehiculo --placas ABC1234 --sandbox

Los parámetros de tipo archivo reciben una ruta. Los que reciben listas de objetos u objetos aceptan JSON
o ``@archivo.json``; las listas de texto se separan con comas.

.. warning::

    No use ``--sandbox`` como garantía en operaciones que crean, modifican o eliminan
    (``cuenta crear-token``, ``ai plantilla-*``, ``ai procesar-*`` e ``imss idse-*``).

Inteligencia artificial
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Comando
     - Descripción
   * - ``ai dataset-fila``
     - Consulta una fila de un dataset.
   * - ``ai dataset-filas``
     - Consulta las filas de un dataset.
   * - ``ai datasets``
     - Lista los datasets del token.
   * - ``ai ocr-id``
     - Extrae los datos de una identificación (JPG, PNG o PDF, hasta 20 MB).
   * - ``ai plantilla-actualizar``
     - Reemplaza el contenido de una plantilla.
   * - ``ai plantilla-crear``
     - Sube una plantilla PDFMe en formato JSON.
   * - ``ai plantilla-generar``
     - Genera un PDF a partir de una plantilla.
   * - ``ai procesar-ejecutar``
     - Ejecuta el procesamiento de un dataset. Consume saldo.
   * - ``ai procesar-eliminar``
     - Elimina un dataset y sus transacciones. No se puede deshacer.
   * - ``ai procesar-estado``
     - Consulta el estado de las transacciones de procesamiento.
   * - ``ai procesar-estimar``
     - Estima el costo de procesar un dataset.
   * - ``ai procesar-exportar``
     - Exporta los resultados del procesamiento.
   * - ``ai procesar-planear``
     - Define los servicios que enriquecen un dataset.
   * - ``ai procesar-subir``
     - Sube un archivo CSV para su procesamiento.

Cuenta
~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Comando
     - Descripción
   * - ``cuenta crear-token``
     - Crea un token en la cuenta.
   * - ``cuenta llave-publica``
     - Obtiene la llave pública de API Market.
   * - ``cuenta saldo``
     - Consulta el saldo disponible de la cuenta.

Geolocalización
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Comando
     - Descripción
   * - ``geo codigos-postales``
     - Busca códigos postales.

IMSS e IDSE
~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Comando
     - Descripción
   * - ``imss datos-nss``
     - Obtiene los datos asociados a un NSS.
   * - ``imss historial-laboral-lite``
     - Solicita el historial laboral en versión ligera.
   * - ``imss idse-capturar``
     - Envía movimientos afiliatorios a IDSE.
   * - ``imss idse-consultar``
     - Consulta el resultado de un lote de movimientos afiliatorios.
   * - ``imss idse-registros-patronales``
     - Solicita los registros patronales disponibles en IDSE.
   * - ``imss pension``
     - Consulta la pensión del IMSS por NSS.
   * - ``imss rpci``
     - Consulta el servicio RPCI del IMSS.
   * - ``imss trayectoria-laboral``
     - Genera el reporte de trayectoria laboral.
   * - ``imss umf-asignada``
     - Consulta la UMF asignada a un NSS.

INFONAVIT
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Comando
     - Descripción
   * - ``infonavit datos-acreditado``
     - Obtiene los datos del acreditado.
   * - ``infonavit datos-cobranza``
     - Consulta los datos de cobranza de un crédito.
   * - ``infonavit datos-contacto``
     - Obtiene los datos de contacto por NSS.
   * - ``infonavit datos-financieros``
     - Consulta los datos financieros de un crédito.
   * - ``infonavit estado-cuenta``
     - Obtiene el estado de cuenta de un crédito.
   * - ``infonavit ficha-tecnica``
     - Genera la ficha técnica del crédito.
   * - ``infonavit historico``
     - Consulta el histórico de un crédito.
   * - ``infonavit reporte-historico``
     - Obtiene el reporte histórico de un crédito.
   * - ``infonavit reporte-intereses``
     - Obtiene el reporte de intereses de un crédito.

RENAPO
~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Comando
     - Descripción
   * - ``renapo acta-nacimiento``
     - Obtiene el acta de nacimiento por CURP.

REPUVE
~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Comando
     - Descripción
   * - ``repuve propietario``
     - Consulta el propietario de un vehículo por número de serie o placas.
   * - ``repuve robo``
     - Consulta si un vehículo tiene reporte de robo.
   * - ``repuve vehiculo``
     - Consulta los datos de un vehículo por número de serie o placas.

SAT
~~~

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Comando
     - Descripción
   * - ``sat buzon-leer``
     - Abre un mensaje del buzón tributario.
   * - ``sat buzon-leidos``
     - Lista los mensajes leídos del buzón tributario.
   * - ``sat buzon-medios-contacto``
     - Consulta los medios de contacto del buzón tributario.
   * - ``sat buzon-nuevos``
     - Lista los mensajes nuevos del buzón tributario.
   * - ``sat certificados-efirma``
     - Lista los certificados de e.firma.
   * - ``sat certificados-rfc``
     - Obtiene los certificados asociados a un RFC.
   * - ``sat certificados-sello-digital``
     - Lista los certificados de sello digital.
   * - ``sat cif``
     - Obtiene la Cédula de Identificación Fiscal.
   * - ``sat csf``
     - Obtiene la Constancia de Situación Fiscal.
   * - ``sat datos-idcif``
     - Obtiene los datos fiscales con el RFC y el idCIF.
   * - ``sat declaracion-acuse``
     - Descarga el acuse de una declaración.
   * - ``sat declaracion-representacion``
     - Obtiene la representación impresa de una declaración.
   * - ``sat declaraciones``
     - Lista las declaraciones de un ejercicio.
   * - ``sat facturacion-perfil``
     - Consulta el perfil de facturación.
   * - ``sat facturas-buscar``
     - Busca CFDI en el portal de facturación del SAT.
   * - ``sat facturas-descargar``
     - Descarga un CFDI.
   * - ``sat informacion``
     - Consulta la información general del contribuyente.
   * - ``sat leer-csf``
     - Extrae los datos de una Constancia de Situación Fiscal (PDF o imagen).
   * - ``sat opinion-cumplimiento``
     - Obtiene la opinión de cumplimiento (32-D).
   * - ``sat validar-receptor``
     - Valida los datos fiscales de un receptor de CFDI contra el padrón.
   * - ``sat validar-rfc``
     - Valida un RFC ante el SAT.
   * - ``sat verificar-efirma``
     - Verifica una firma electrónica.

SEP
~~~

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Comando
     - Descripción
   * - ``sep constancia-profesional``
     - Descarga la constancia profesional de la SEP por CURP.

----

Manejo de errores
-----------------

Todos los comandos muestran los errores como ``Error [CÓDIGO]: mensaje`` en la salida de errores. Salen con
código 2 si los argumentos son incorrectos y con 1 en los demás casos.

.. code-block:: bash

    $ apimarket -vc INVALIDA
    Error [INVALID_CURP_LENGTH]: Longitud inválida: se esperaban 18 caracteres, se recibieron 8.

    $ apimarket sat leer-csf --csf no-existe.pdf
    Error [FILE_NOT_FOUND]: No existe el archivo 'no-existe.pdf'.

    $ apimarket cuenta saldo
    {"success": false, "codigoValidacion": "...", "message": "El token proporcionado no es valido.", "status": 401}
    Error [API_KEY_UNAUTHORIZED]: El token proporcionado no es valido. (status 401)

    $ apimarket errores        # catálogo completo

Para el catálogo completo de códigos de error ver :doc:`error_catalog`.
