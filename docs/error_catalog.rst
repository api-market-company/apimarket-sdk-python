Error Catalog
=============

Todos los errores que entrega el SDK llevan un atributo ``code`` (miembro de un ``Enum``) y un mensaje en español.
La misma lista se consulta con ``apimarket errores`` y está definida en ``apimarket/errors.py``.

Formato de los códigos
----------------------

.. list-table::
   :header-rows: 1
   :widths: 22 38 40

   * - Origen
     - Formato
     - Ejemplos
   * - Dato inválido
     - ``INVALID_<CAMPO>_<MOTIVO>``
     - ``INVALID_CURP_LENGTH``, ``INVALID_CP_LENGTH``
   * - Archivo inválido
     - ``INVALID_<CAMPO>_FILE_<MOTIVO>``
     - ``INVALID_CSF_FILE_NOT_FOUND``
   * - Configuración
     - ``CONFIG_<DATO>_MISSING``
     - ``CONFIG_API_KEY_MISSING``
   * - Respuesta de la API
     - ``API_<ASUNTO>_<MOTIVO>``
     - ``API_KEY_UNAUTHORIZED``
   * - Red
     - ``NETWORK_<ASUNTO>_<MOTIVO>``
     - ``NETWORK_RESPONSE_TIMEOUT``
   * - Línea de comandos
     - ``CLI_<ASUNTO>_<MOTIVO>``
     - ``CLI_ARGUMENTS_INVALID``

En ``<CAMPO>`` va el nombre del parámetro en mayúsculas (``movimientos[0].apellidoPaterno`` es
``MOVIMIENTOS_APELLIDO_PATERNO``). Los motivos son ``MISSING``, ``TYPE``, ``LENGTH``, ``RANGE``, ``FORMAT``,
``DIGIT``, ``OPTION``, ``COMBINATION`` y ``PATH``; en archivos, ``NOT_FOUND``, ``UNREADABLE``, ``EMPTY``, ``TYPE``,
``SIZE`` y ``CONTENT``.

Cómo se agrupan
---------------

.. list-table::
   :header-rows: 1
   :widths: 20 60 20

   * - Origen
     - Excepción
     - Se envía la petición
   * - Validación local
     - Subclases de ``apimarket.ValidationError`` (heredan de ``ValueError``)
     - No
   * - Respuesta de la API
     - ``APIError``; en los servicios por grupo, ``apimarket.ApiMarketError``
     - Sí
   * - Red
     - Excepciones de ``httpx.HTTPError``
     - No se completa

----

CURP — ``InvalidCURPError``
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 34 38

   * - Código
     - Miembro del Enum
     - Descripción
   * - ``INVALID_CURP_LENGTH``
     - ``InvalidCURPError.Code.INVALID_LENGTH``
     - La CURP no tiene exactamente 18 caracteres.
   * - ``INVALID_CURP_FORMAT``
     - ``InvalidCURPError.Code.INVALID_FORMAT``
     - La CURP no cumple el patrón oficial.
   * - ``INVALID_CURP_DIGIT``
     - ``InvalidCURPError.Code.INVALID_DIGIT``
     - El dígito verificador de la CURP no corresponde.

----

RFC — ``InvalidRFCError``
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 34 38

   * - Código
     - Miembro del Enum
     - Descripción
   * - ``INVALID_RFC_FORMAT``
     - ``InvalidRFCError.Code.INVALID_FORMAT``
     - El RFC no cumple el patrón de persona física o moral, en mayúsculas.

----

NSS — ``InvalidNSSError``
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 34 38

   * - Código
     - Miembro del Enum
     - Descripción
   * - ``INVALID_NSS_LENGTH``
     - ``InvalidNSSError.Code.INVALID_LENGTH``
     - El NSS no tiene exactamente 11 dígitos.
   * - ``INVALID_NSS_FORMAT``
     - ``InvalidNSSError.Code.INVALID_FORMAT``
     - El NSS contiene caracteres no numéricos.
   * - ``INVALID_NSS_DIGIT``
     - ``InvalidNSSError.Code.INVALID_DIGIT``
     - El dígito verificador del NSS no corresponde.

----

Fecha de nacimiento — ``InvalidBirthDateError``
-----------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 34 38

   * - Código
     - Miembro del Enum
     - Descripción
   * - ``INVALID_BIRTH_DAY_FORMAT``
     - ``InvalidBirthDateError.Code.INVALID_BIRTH_DAY_FORMAT``
     - El día no tiene exactamente 2 dígitos.
   * - ``INVALID_BIRTH_MONTH_FORMAT``
     - ``InvalidBirthDateError.Code.INVALID_BIRTH_MONTH_FORMAT``
     - El mes no tiene exactamente 2 dígitos.
   * - ``INVALID_BIRTH_YEAR_FORMAT``
     - ``InvalidBirthDateError.Code.INVALID_BIRTH_YEAR_FORMAT``
     - El año no tiene exactamente 4 dígitos.

----

Folio de certificado — ``InvalidFolioError``
--------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 34 38

   * - Código
     - Miembro del Enum
     - Descripción
   * - ``INVALID_FOLIO_FORMAT``
     - ``InvalidFolioError.Code.INVALID_FORMAT``
     - El folio no es un UUID.

----

Número de crédito INFONAVIT — ``InvalidCreditError``
----------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 34 38

   * - Código
     - Miembro del Enum
     - Descripción
   * - ``INVALID_CREDIT_FORMAT``
     - ``InvalidCreditError.Code.INVALID_FORMAT``
     - El número de crédito no tiene exactamente 10 dígitos.

----

Parámetros — ``InvalidParameterError``
--------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 34 38

   * - Código
     - Miembro del Enum
     - Descripción
   * - ``INVALID_ANVERSO_MISSING``
     - ``InvalidParameterError.Code.ANVERSO_MISSING``
     - Falta 'anverso' o llegó vacío.
   * - ``INVALID_ANVERSO_TYPE``
     - ``InvalidParameterError.Code.ANVERSO_TYPE``
     - 'anverso' no tiene el tipo de dato esperado.
   * - ``INVALID_BLOB_PATH_MISSING``
     - ``InvalidParameterError.Code.BLOB_PATH_MISSING``
     - Falta 'blob_path' o llegó vacío.
   * - ``INVALID_BLOB_PATH_TYPE``
     - ``InvalidParameterError.Code.BLOB_PATH_TYPE``
     - 'blob_path' no tiene el tipo de dato esperado.
   * - ``INVALID_BLOB_PATH_LENGTH``
     - ``InvalidParameterError.Code.BLOB_PATH_LENGTH``
     - La longitud o cantidad de 'blob_path' está fuera de los límites.
   * - ``INVALID_BLOB_PATH_FORMAT``
     - ``InvalidParameterError.Code.BLOB_PATH_FORMAT``
     - 'blob_path' no tiene el formato esperado.
   * - ``INVALID_CEDULA_MISSING``
     - ``InvalidParameterError.Code.CEDULA_MISSING``
     - Falta 'cedula' o llegó vacío.
   * - ``INVALID_CEDULA_TYPE``
     - ``InvalidParameterError.Code.CEDULA_TYPE``
     - 'cedula' no tiene el tipo de dato esperado.
   * - ``INVALID_CEDULA_FORMAT``
     - ``InvalidParameterError.Code.CEDULA_FORMAT``
     - 'cedula' no tiene el formato esperado.
   * - ``INVALID_CERTIFICATE_MISSING``
     - ``InvalidParameterError.Code.CERTIFICATE_MISSING``
     - Falta 'certificate' o llegó vacío.
   * - ``INVALID_CERTIFICATE_TYPE``
     - ``InvalidParameterError.Code.CERTIFICATE_TYPE``
     - 'certificate' no tiene el tipo de dato esperado.
   * - ``INVALID_CIEC_MISSING``
     - ``InvalidParameterError.Code.CIEC_MISSING``
     - Falta 'ciec' o llegó vacío.
   * - ``INVALID_CIEC_TYPE``
     - ``InvalidParameterError.Code.CIEC_TYPE``
     - 'ciec' no tiene el tipo de dato esperado.
   * - ``INVALID_CIEC_LENGTH``
     - ``InvalidParameterError.Code.CIEC_LENGTH``
     - La longitud o cantidad de 'ciec' está fuera de los límites.
   * - ``INVALID_CLAVE_ENTIDAD_MISSING``
     - ``InvalidParameterError.Code.CLAVE_ENTIDAD_MISSING``
     - Falta 'clave_entidad' o llegó vacío.
   * - ``INVALID_CLAVE_ENTIDAD_TYPE``
     - ``InvalidParameterError.Code.CLAVE_ENTIDAD_TYPE``
     - 'clave_entidad' no tiene el tipo de dato esperado.
   * - ``INVALID_CLAVE_ENTIDAD_OPTION``
     - ``InvalidParameterError.Code.CLAVE_ENTIDAD_OPTION``
     - 'clave_entidad' no está entre las opciones permitidas.
   * - ``INVALID_CODIGO_POSTAL_MISSING``
     - ``InvalidParameterError.Code.CODIGO_POSTAL_MISSING``
     - Falta 'codigo_postal' o llegó vacío.
   * - ``INVALID_CODIGO_POSTAL_TYPE``
     - ``InvalidParameterError.Code.CODIGO_POSTAL_TYPE``
     - 'codigo_postal' no tiene el tipo de dato esperado.
   * - ``INVALID_CODIGO_POSTAL_LENGTH``
     - ``InvalidParameterError.Code.CODIGO_POSTAL_LENGTH``
     - La longitud o cantidad de 'codigo_postal' está fuera de los límites.
   * - ``INVALID_CODIGO_POSTAL_FORMAT``
     - ``InvalidParameterError.Code.CODIGO_POSTAL_FORMAT``
     - 'codigo_postal' no tiene el formato esperado.
   * - ``INVALID_CODIGO_VALIDACION_RELACIONADO_MISSING``
     - ``InvalidParameterError.Code.CODIGO_VALIDACION_RELACIONADO_MISSING``
     - Falta 'codigo_validacion_relacionado' o llegó vacío.
   * - ``INVALID_CODIGO_VALIDACION_RELACIONADO_TYPE``
     - ``InvalidParameterError.Code.CODIGO_VALIDACION_RELACIONADO_TYPE``
     - 'codigo_validacion_relacionado' no tiene el tipo de dato esperado.
   * - ``INVALID_CODIGO_VALIDACION_RELACIONADO_LENGTH``
     - ``InvalidParameterError.Code.CODIGO_VALIDACION_RELACIONADO_LENGTH``
     - La longitud o cantidad de 'codigo_validacion_relacionado' está fuera de los límites.
   * - ``INVALID_COMPANY_MISSING``
     - ``InvalidParameterError.Code.COMPANY_MISSING``
     - Falta 'company' o llegó vacío.
   * - ``INVALID_COMPANY_TYPE``
     - ``InvalidParameterError.Code.COMPANY_TYPE``
     - 'company' no tiene el tipo de dato esperado.
   * - ``INVALID_COMPLEMENTOS_MISSING``
     - ``InvalidParameterError.Code.COMPLEMENTOS_MISSING``
     - Falta 'complementos' o llegó vacío.
   * - ``INVALID_COMPLEMENTOS_TYPE``
     - ``InvalidParameterError.Code.COMPLEMENTOS_TYPE``
     - 'complementos' no tiene el tipo de dato esperado.
   * - ``INVALID_COMPLEMENTOS_LENGTH``
     - ``InvalidParameterError.Code.COMPLEMENTOS_LENGTH``
     - La longitud o cantidad de 'complementos' está fuera de los límites.
   * - ``INVALID_CORREO_MISSING``
     - ``InvalidParameterError.Code.CORREO_MISSING``
     - Falta 'correo' o llegó vacío.
   * - ``INVALID_CORREO_TYPE``
     - ``InvalidParameterError.Code.CORREO_TYPE``
     - 'correo' no tiene el tipo de dato esperado.
   * - ``INVALID_CORREO_LENGTH``
     - ``InvalidParameterError.Code.CORREO_LENGTH``
     - La longitud o cantidad de 'correo' está fuera de los límites.
   * - ``INVALID_CORREO_FORMAT``
     - ``InvalidParameterError.Code.CORREO_FORMAT``
     - 'correo' no tiene el formato esperado.
   * - ``INVALID_COUNTRY_CODE_MISSING``
     - ``InvalidParameterError.Code.COUNTRY_CODE_MISSING``
     - Falta 'country_code' o llegó vacío.
   * - ``INVALID_COUNTRY_CODE_TYPE``
     - ``InvalidParameterError.Code.COUNTRY_CODE_TYPE``
     - 'country_code' no tiene el tipo de dato esperado.
   * - ``INVALID_COUNTRY_CODE_FORMAT``
     - ``InvalidParameterError.Code.COUNTRY_CODE_FORMAT``
     - 'country_code' no tiene el formato esperado.
   * - ``INVALID_CP_MISSING``
     - ``InvalidParameterError.Code.CP_MISSING``
     - Falta 'cp' o llegó vacío.
   * - ``INVALID_CP_TYPE``
     - ``InvalidParameterError.Code.CP_TYPE``
     - 'cp' no tiene el tipo de dato esperado.
   * - ``INVALID_CP_LENGTH``
     - ``InvalidParameterError.Code.CP_LENGTH``
     - La longitud o cantidad de 'cp' está fuera de los límites.
   * - ``INVALID_CP_FORMAT``
     - ``InvalidParameterError.Code.CP_FORMAT``
     - 'cp' no tiene el formato esperado.
   * - ``INVALID_CREDENTIALS_MISSING``
     - ``InvalidParameterError.Code.CREDENTIALS_MISSING``
     - Falta 'credentials' o llegó vacío.
   * - ``INVALID_CREDENTIALS_TYPE``
     - ``InvalidParameterError.Code.CREDENTIALS_TYPE``
     - 'credentials' no tiene el tipo de dato esperado.
   * - ``INVALID_CREDENTIALS_CERTIFICATE_MISSING``
     - ``InvalidParameterError.Code.CREDENTIALS_CERTIFICATE_MISSING``
     - Falta 'credentials_certificate' o llegó vacío.
   * - ``INVALID_CREDENTIALS_CERTIFICATE_TYPE``
     - ``InvalidParameterError.Code.CREDENTIALS_CERTIFICATE_TYPE``
     - 'credentials_certificate' no tiene el tipo de dato esperado.
   * - ``INVALID_CREDENTIALS_CERTIFICATE_FORMAT``
     - ``InvalidParameterError.Code.CREDENTIALS_CERTIFICATE_FORMAT``
     - 'credentials_certificate' no tiene el formato esperado.
   * - ``INVALID_CREDENTIALS_PASSWORD_MISSING``
     - ``InvalidParameterError.Code.CREDENTIALS_PASSWORD_MISSING``
     - Falta 'credentials_password' o llegó vacío.
   * - ``INVALID_CREDENTIALS_PASSWORD_TYPE``
     - ``InvalidParameterError.Code.CREDENTIALS_PASSWORD_TYPE``
     - 'credentials_password' no tiene el tipo de dato esperado.
   * - ``INVALID_CREDENTIALS_PASSWORD_FORMAT``
     - ``InvalidParameterError.Code.CREDENTIALS_PASSWORD_FORMAT``
     - 'credentials_password' no tiene el formato esperado.
   * - ``INVALID_CREDENTIALS_PRIVATE_KEY_MISSING``
     - ``InvalidParameterError.Code.CREDENTIALS_PRIVATE_KEY_MISSING``
     - Falta 'credentials_private_key' o llegó vacío.
   * - ``INVALID_CREDENTIALS_PRIVATE_KEY_TYPE``
     - ``InvalidParameterError.Code.CREDENTIALS_PRIVATE_KEY_TYPE``
     - 'credentials_private_key' no tiene el tipo de dato esperado.
   * - ``INVALID_CREDENTIALS_PRIVATE_KEY_FORMAT``
     - ``InvalidParameterError.Code.CREDENTIALS_PRIVATE_KEY_FORMAT``
     - 'credentials_private_key' no tiene el formato esperado.
   * - ``INVALID_CREDENTIALS_USER_ID_MISSING``
     - ``InvalidParameterError.Code.CREDENTIALS_USER_ID_MISSING``
     - Falta 'credentials_user_id' o llegó vacío.
   * - ``INVALID_CREDENTIALS_USER_ID_TYPE``
     - ``InvalidParameterError.Code.CREDENTIALS_USER_ID_TYPE``
     - 'credentials_user_id' no tiene el tipo de dato esperado.
   * - ``INVALID_CREDENTIALS_USER_ID_FORMAT``
     - ``InvalidParameterError.Code.CREDENTIALS_USER_ID_FORMAT``
     - 'credentials_user_id' no tiene el formato esperado.
   * - ``INVALID_CSF_MISSING``
     - ``InvalidParameterError.Code.CSF_MISSING``
     - Falta 'csf' o llegó vacío.
   * - ``INVALID_CSF_TYPE``
     - ``InvalidParameterError.Code.CSF_TYPE``
     - 'csf' no tiene el tipo de dato esperado.
   * - ``INVALID_CURP_MISSING``
     - ``InvalidParameterError.Code.CURP_MISSING``
     - Falta 'curp' o llegó vacío.
   * - ``INVALID_CURP_TYPE``
     - ``InvalidParameterError.Code.CURP_TYPE``
     - 'curp' no tiene el tipo de dato esperado.
   * - ``INVALID_DATA_MISSING``
     - ``InvalidParameterError.Code.DATA_MISSING``
     - Falta 'data' o llegó vacío.
   * - ``INVALID_DATA_TYPE``
     - ``InvalidParameterError.Code.DATA_TYPE``
     - 'data' no tiene el tipo de dato esperado.
   * - ``INVALID_DATASET_MISSING``
     - ``InvalidParameterError.Code.DATASET_MISSING``
     - Falta 'dataset' o llegó vacío.
   * - ``INVALID_DATASET_TYPE``
     - ``InvalidParameterError.Code.DATASET_TYPE``
     - 'dataset' no tiene el tipo de dato esperado.
   * - ``INVALID_DELAY_MISSING``
     - ``InvalidParameterError.Code.DELAY_MISSING``
     - Falta 'delay' o llegó vacío.
   * - ``INVALID_DELAY_TYPE``
     - ``InvalidParameterError.Code.DELAY_TYPE``
     - 'delay' no tiene el tipo de dato esperado.
   * - ``INVALID_DELAY_FORMAT``
     - ``InvalidParameterError.Code.DELAY_FORMAT``
     - 'delay' no tiene el formato esperado.
   * - ``INVALID_DESCRIPTION_MISSING``
     - ``InvalidParameterError.Code.DESCRIPTION_MISSING``
     - Falta 'description' o llegó vacío.
   * - ``INVALID_DESCRIPTION_TYPE``
     - ``InvalidParameterError.Code.DESCRIPTION_TYPE``
     - 'description' no tiene el tipo de dato esperado.
   * - ``INVALID_EMAIL_MISSING``
     - ``InvalidParameterError.Code.EMAIL_MISSING``
     - Falta 'email' o llegó vacío.
   * - ``INVALID_EMAIL_TYPE``
     - ``InvalidParameterError.Code.EMAIL_TYPE``
     - 'email' no tiene el tipo de dato esperado.
   * - ``INVALID_EMAIL_LENGTH``
     - ``InvalidParameterError.Code.EMAIL_LENGTH``
     - La longitud o cantidad de 'email' está fuera de los límites.
   * - ``INVALID_EMAIL_FORMAT``
     - ``InvalidParameterError.Code.EMAIL_FORMAT``
     - 'email' no tiene el formato esperado.
   * - ``INVALID_ESTADO_COMPROBANTE_MISSING``
     - ``InvalidParameterError.Code.ESTADO_COMPROBANTE_MISSING``
     - Falta 'estado_comprobante' o llegó vacío.
   * - ``INVALID_ESTADO_COMPROBANTE_TYPE``
     - ``InvalidParameterError.Code.ESTADO_COMPROBANTE_TYPE``
     - 'estado_comprobante' no tiene el tipo de dato esperado.
   * - ``INVALID_FECHA_FINAL_MISSING``
     - ``InvalidParameterError.Code.FECHA_FINAL_MISSING``
     - Falta 'fecha_final' o llegó vacío.
   * - ``INVALID_FECHA_FINAL_TYPE``
     - ``InvalidParameterError.Code.FECHA_FINAL_TYPE``
     - 'fecha_final' no tiene el tipo de dato esperado.
   * - ``INVALID_FECHA_FINAL_RANGE``
     - ``InvalidParameterError.Code.FECHA_FINAL_RANGE``
     - El valor de 'fecha_final' está fuera del rango permitido.
   * - ``INVALID_FECHA_FINAL_FORMAT``
     - ``InvalidParameterError.Code.FECHA_FINAL_FORMAT``
     - 'fecha_final' no tiene el formato esperado.
   * - ``INVALID_FECHA_FINAL_COMBINATION``
     - ``InvalidParameterError.Code.FECHA_FINAL_COMBINATION``
     - 'fecha_final' no es compatible con los demás parámetros.
   * - ``INVALID_FECHA_INICIAL_MISSING``
     - ``InvalidParameterError.Code.FECHA_INICIAL_MISSING``
     - Falta 'fecha_inicial' o llegó vacío.
   * - ``INVALID_FECHA_INICIAL_TYPE``
     - ``InvalidParameterError.Code.FECHA_INICIAL_TYPE``
     - 'fecha_inicial' no tiene el tipo de dato esperado.
   * - ``INVALID_FECHA_INICIAL_FORMAT``
     - ``InvalidParameterError.Code.FECHA_INICIAL_FORMAT``
     - 'fecha_inicial' no tiene el formato esperado.
   * - ``INVALID_FILTER_MISSING``
     - ``InvalidParameterError.Code.FILTER_MISSING``
     - Falta 'filter' o llegó vacío.
   * - ``INVALID_FILTER_TYPE``
     - ``InvalidParameterError.Code.FILTER_TYPE``
     - 'filter' no tiene el tipo de dato esperado.
   * - ``INVALID_FILTER_OPTION``
     - ``InvalidParameterError.Code.FILTER_OPTION``
     - 'filter' no está entre las opciones permitidas.
   * - ``INVALID_FOLIO_MISSING``
     - ``InvalidParameterError.Code.FOLIO_MISSING``
     - Falta 'folio' o llegó vacío.
   * - ``INVALID_FOLIO_TYPE``
     - ``InvalidParameterError.Code.FOLIO_TYPE``
     - 'folio' no tiene el tipo de dato esperado.
   * - ``INVALID_FORMATO_MISSING``
     - ``InvalidParameterError.Code.FORMATO_MISSING``
     - Falta 'formato' o llegó vacío.
   * - ``INVALID_FORMATO_TYPE``
     - ``InvalidParameterError.Code.FORMATO_TYPE``
     - 'formato' no tiene el tipo de dato esperado.
   * - ``INVALID_FORMATO_OPTION``
     - ``InvalidParameterError.Code.FORMATO_OPTION``
     - 'formato' no está entre las opciones permitidas.
   * - ``INVALID_IDCIF_MISSING``
     - ``InvalidParameterError.Code.IDCIF_MISSING``
     - Falta 'idcif' o llegó vacío.
   * - ``INVALID_IDCIF_TYPE``
     - ``InvalidParameterError.Code.IDCIF_TYPE``
     - 'idcif' no tiene el tipo de dato esperado.
   * - ``INVALID_IDCIF_FORMAT``
     - ``InvalidParameterError.Code.IDCIF_FORMAT``
     - 'idcif' no tiene el formato esperado.
   * - ``INVALID_IDENTIFICADOR_MISSING``
     - ``InvalidParameterError.Code.IDENTIFICADOR_MISSING``
     - Falta 'identificador' o llegó vacío.
   * - ``INVALID_IDENTIFICADOR_TYPE``
     - ``InvalidParameterError.Code.IDENTIFICADOR_TYPE``
     - 'identificador' no tiene el tipo de dato esperado.
   * - ``INVALID_IDENTIFICADOR_FORMAT``
     - ``InvalidParameterError.Code.IDENTIFICADOR_FORMAT``
     - 'identificador' no tiene el formato esperado.
   * - ``INVALID_INPUTS_MISSING``
     - ``InvalidParameterError.Code.INPUTS_MISSING``
     - Falta 'inputs' o llegó vacío.
   * - ``INVALID_INPUTS_TYPE``
     - ``InvalidParameterError.Code.INPUTS_TYPE``
     - 'inputs' no tiene el tipo de dato esperado.
   * - ``INVALID_INPUTS_LENGTH``
     - ``InvalidParameterError.Code.INPUTS_LENGTH``
     - La longitud o cantidad de 'inputs' está fuera de los límites.
   * - ``INVALID_LOTE_MISSING``
     - ``InvalidParameterError.Code.LOTE_MISSING``
     - Falta 'lote' o llegó vacío.
   * - ``INVALID_LOTE_TYPE``
     - ``InvalidParameterError.Code.LOTE_TYPE``
     - 'lote' no tiene el tipo de dato esperado.
   * - ``INVALID_LOTE_RANGE``
     - ``InvalidParameterError.Code.LOTE_RANGE``
     - El valor de 'lote' está fuera del rango permitido.
   * - ``INVALID_MATERNO_MISSING``
     - ``InvalidParameterError.Code.MATERNO_MISSING``
     - Falta 'materno' o llegó vacío.
   * - ``INVALID_MATERNO_TYPE``
     - ``InvalidParameterError.Code.MATERNO_TYPE``
     - 'materno' no tiene el tipo de dato esperado.
   * - ``INVALID_MOVIMIENTOS_MISSING``
     - ``InvalidParameterError.Code.MOVIMIENTOS_MISSING``
     - Falta 'movimientos' o llegó vacío.
   * - ``INVALID_MOVIMIENTOS_TYPE``
     - ``InvalidParameterError.Code.MOVIMIENTOS_TYPE``
     - 'movimientos' no tiene el tipo de dato esperado.
   * - ``INVALID_MOVIMIENTOS_APELLIDO_MATERNO_MISSING``
     - ``InvalidParameterError.Code.MOVIMIENTOS_APELLIDO_MATERNO_MISSING``
     - Falta 'movimientos_apellido_materno' o llegó vacío.
   * - ``INVALID_MOVIMIENTOS_APELLIDO_MATERNO_TYPE``
     - ``InvalidParameterError.Code.MOVIMIENTOS_APELLIDO_MATERNO_TYPE``
     - 'movimientos_apellido_materno' no tiene el tipo de dato esperado.
   * - ``INVALID_MOVIMIENTOS_APELLIDO_MATERNO_LENGTH``
     - ``InvalidParameterError.Code.MOVIMIENTOS_APELLIDO_MATERNO_LENGTH``
     - La longitud o cantidad de 'movimientos_apellido_materno' está fuera de los límites.
   * - ``INVALID_MOVIMIENTOS_APELLIDO_PATERNO_MISSING``
     - ``InvalidParameterError.Code.MOVIMIENTOS_APELLIDO_PATERNO_MISSING``
     - Falta 'movimientos_apellido_paterno' o llegó vacío.
   * - ``INVALID_MOVIMIENTOS_APELLIDO_PATERNO_TYPE``
     - ``InvalidParameterError.Code.MOVIMIENTOS_APELLIDO_PATERNO_TYPE``
     - 'movimientos_apellido_paterno' no tiene el tipo de dato esperado.
   * - ``INVALID_MOVIMIENTOS_APELLIDO_PATERNO_LENGTH``
     - ``InvalidParameterError.Code.MOVIMIENTOS_APELLIDO_PATERNO_LENGTH``
     - La longitud o cantidad de 'movimientos_apellido_paterno' está fuera de los límites.
   * - ``INVALID_MOVIMIENTOS_CAUSA_DE_BAJA_MISSING``
     - ``InvalidParameterError.Code.MOVIMIENTOS_CAUSA_DE_BAJA_MISSING``
     - Falta 'movimientos_causa_de_baja' o llegó vacío.
   * - ``INVALID_MOVIMIENTOS_CAUSA_DE_BAJA_TYPE``
     - ``InvalidParameterError.Code.MOVIMIENTOS_CAUSA_DE_BAJA_TYPE``
     - 'movimientos_causa_de_baja' no tiene el tipo de dato esperado.
   * - ``INVALID_MOVIMIENTOS_CAUSA_DE_BAJA_OPTION``
     - ``InvalidParameterError.Code.MOVIMIENTOS_CAUSA_DE_BAJA_OPTION``
     - 'movimientos_causa_de_baja' no está entre las opciones permitidas.
   * - ``INVALID_MOVIMIENTOS_CLAVE_DEL_TRABAJADOR_FORMAT``
     - ``InvalidParameterError.Code.MOVIMIENTOS_CLAVE_DEL_TRABAJADOR_FORMAT``
     - 'movimientos_clave_del_trabajador' no tiene el formato esperado.
   * - ``INVALID_MOVIMIENTOS_FECHA_DE_MOVIMIENTO_MISSING``
     - ``InvalidParameterError.Code.MOVIMIENTOS_FECHA_DE_MOVIMIENTO_MISSING``
     - Falta 'movimientos_fecha_de_movimiento' o llegó vacío.
   * - ``INVALID_MOVIMIENTOS_FECHA_DE_MOVIMIENTO_TYPE``
     - ``InvalidParameterError.Code.MOVIMIENTOS_FECHA_DE_MOVIMIENTO_TYPE``
     - 'movimientos_fecha_de_movimiento' no tiene el tipo de dato esperado.
   * - ``INVALID_MOVIMIENTOS_FECHA_DE_MOVIMIENTO_FORMAT``
     - ``InvalidParameterError.Code.MOVIMIENTOS_FECHA_DE_MOVIMIENTO_FORMAT``
     - 'movimientos_fecha_de_movimiento' no tiene el formato esperado.
   * - ``INVALID_MOVIMIENTOS_JORNADA_MISSING``
     - ``InvalidParameterError.Code.MOVIMIENTOS_JORNADA_MISSING``
     - Falta 'movimientos_jornada' o llegó vacío.
   * - ``INVALID_MOVIMIENTOS_JORNADA_TYPE``
     - ``InvalidParameterError.Code.MOVIMIENTOS_JORNADA_TYPE``
     - 'movimientos_jornada' no tiene el tipo de dato esperado.
   * - ``INVALID_MOVIMIENTOS_JORNADA_OPTION``
     - ``InvalidParameterError.Code.MOVIMIENTOS_JORNADA_OPTION``
     - 'movimientos_jornada' no está entre las opciones permitidas.
   * - ``INVALID_MOVIMIENTOS_NOMBRE_MISSING``
     - ``InvalidParameterError.Code.MOVIMIENTOS_NOMBRE_MISSING``
     - Falta 'movimientos_nombre' o llegó vacío.
   * - ``INVALID_MOVIMIENTOS_NOMBRE_TYPE``
     - ``InvalidParameterError.Code.MOVIMIENTOS_NOMBRE_TYPE``
     - 'movimientos_nombre' no tiene el tipo de dato esperado.
   * - ``INVALID_MOVIMIENTOS_NOMBRE_LENGTH``
     - ``InvalidParameterError.Code.MOVIMIENTOS_NOMBRE_LENGTH``
     - La longitud o cantidad de 'movimientos_nombre' está fuera de los límites.
   * - ``INVALID_MOVIMIENTOS_NSS_MISSING``
     - ``InvalidParameterError.Code.MOVIMIENTOS_NSS_MISSING``
     - Falta 'movimientos_nss' o llegó vacío.
   * - ``INVALID_MOVIMIENTOS_REGISTRO_PATRONAL_MISSING``
     - ``InvalidParameterError.Code.MOVIMIENTOS_REGISTRO_PATRONAL_MISSING``
     - Falta 'movimientos_registro_patronal' o llegó vacío.
   * - ``INVALID_MOVIMIENTOS_REGISTRO_PATRONAL_TYPE``
     - ``InvalidParameterError.Code.MOVIMIENTOS_REGISTRO_PATRONAL_TYPE``
     - 'movimientos_registro_patronal' no tiene el tipo de dato esperado.
   * - ``INVALID_MOVIMIENTOS_REGISTRO_PATRONAL_FORMAT``
     - ``InvalidParameterError.Code.MOVIMIENTOS_REGISTRO_PATRONAL_FORMAT``
     - 'movimientos_registro_patronal' no tiene el formato esperado.
   * - ``INVALID_MOVIMIENTOS_SALARIO_DIARIO_INTEGRADO_MISSING``
     - ``InvalidParameterError.Code.MOVIMIENTOS_SALARIO_DIARIO_INTEGRADO_MISSING``
     - Falta 'movimientos_salario_diario_integrado' o llegó vacío.
   * - ``INVALID_MOVIMIENTOS_SALARIO_DIARIO_INTEGRADO_TYPE``
     - ``InvalidParameterError.Code.MOVIMIENTOS_SALARIO_DIARIO_INTEGRADO_TYPE``
     - 'movimientos_salario_diario_integrado' no tiene el tipo de dato esperado.
   * - ``INVALID_MOVIMIENTOS_TIPO_DE_MOVIMIENTO_MISSING``
     - ``InvalidParameterError.Code.MOVIMIENTOS_TIPO_DE_MOVIMIENTO_MISSING``
     - Falta 'movimientos_tipo_de_movimiento' o llegó vacío.
   * - ``INVALID_MOVIMIENTOS_TIPO_DE_MOVIMIENTO_TYPE``
     - ``InvalidParameterError.Code.MOVIMIENTOS_TIPO_DE_MOVIMIENTO_TYPE``
     - 'movimientos_tipo_de_movimiento' no tiene el tipo de dato esperado.
   * - ``INVALID_MOVIMIENTOS_TIPO_DE_MOVIMIENTO_OPTION``
     - ``InvalidParameterError.Code.MOVIMIENTOS_TIPO_DE_MOVIMIENTO_OPTION``
     - 'movimientos_tipo_de_movimiento' no está entre las opciones permitidas.
   * - ``INVALID_MOVIMIENTOS_TIPO_DE_SALARIO_MISSING``
     - ``InvalidParameterError.Code.MOVIMIENTOS_TIPO_DE_SALARIO_MISSING``
     - Falta 'movimientos_tipo_de_salario' o llegó vacío.
   * - ``INVALID_MOVIMIENTOS_TIPO_DE_SALARIO_TYPE``
     - ``InvalidParameterError.Code.MOVIMIENTOS_TIPO_DE_SALARIO_TYPE``
     - 'movimientos_tipo_de_salario' no tiene el tipo de dato esperado.
   * - ``INVALID_MOVIMIENTOS_TIPO_DE_SALARIO_OPTION``
     - ``InvalidParameterError.Code.MOVIMIENTOS_TIPO_DE_SALARIO_OPTION``
     - 'movimientos_tipo_de_salario' no está entre las opciones permitidas.
   * - ``INVALID_MOVIMIENTOS_TIPO_DE_TRABAJADOR_MISSING``
     - ``InvalidParameterError.Code.MOVIMIENTOS_TIPO_DE_TRABAJADOR_MISSING``
     - Falta 'movimientos_tipo_de_trabajador' o llegó vacío.
   * - ``INVALID_MOVIMIENTOS_TIPO_DE_TRABAJADOR_TYPE``
     - ``InvalidParameterError.Code.MOVIMIENTOS_TIPO_DE_TRABAJADOR_TYPE``
     - 'movimientos_tipo_de_trabajador' no tiene el tipo de dato esperado.
   * - ``INVALID_MOVIMIENTOS_TIPO_DE_TRABAJADOR_OPTION``
     - ``InvalidParameterError.Code.MOVIMIENTOS_TIPO_DE_TRABAJADOR_OPTION``
     - 'movimientos_tipo_de_trabajador' no está entre las opciones permitidas.
   * - ``INVALID_MOVIMIENTOS_UMF_MISSING``
     - ``InvalidParameterError.Code.MOVIMIENTOS_UMF_MISSING``
     - Falta 'movimientos_umf' o llegó vacío.
   * - ``INVALID_MOVIMIENTOS_UMF_TYPE``
     - ``InvalidParameterError.Code.MOVIMIENTOS_UMF_TYPE``
     - 'movimientos_umf' no tiene el tipo de dato esperado.
   * - ``INVALID_MOVIMIENTOS_UMF_LENGTH``
     - ``InvalidParameterError.Code.MOVIMIENTOS_UMF_LENGTH``
     - La longitud o cantidad de 'movimientos_umf' está fuera de los límites.
   * - ``INVALID_MOVIMIENTOS_UMF_FORMAT``
     - ``InvalidParameterError.Code.MOVIMIENTOS_UMF_FORMAT``
     - 'movimientos_umf' no tiene el formato esperado.
   * - ``INVALID_NAME_MISSING``
     - ``InvalidParameterError.Code.NAME_MISSING``
     - Falta 'name' o llegó vacío.
   * - ``INVALID_NAME_TYPE``
     - ``InvalidParameterError.Code.NAME_TYPE``
     - 'name' no tiene el tipo de dato esperado.
   * - ``INVALID_NOMBRE_MISSING``
     - ``InvalidParameterError.Code.NOMBRE_MISSING``
     - Falta 'nombre' o llegó vacío.
   * - ``INVALID_NOMBRE_TYPE``
     - ``InvalidParameterError.Code.NOMBRE_TYPE``
     - 'nombre' no tiene el tipo de dato esperado.
   * - ``INVALID_NOMBRE_LENGTH``
     - ``InvalidParameterError.Code.NOMBRE_LENGTH``
     - La longitud o cantidad de 'nombre' está fuera de los límites.
   * - ``INVALID_NOMBRES_MISSING``
     - ``InvalidParameterError.Code.NOMBRES_MISSING``
     - Falta 'nombres' o llegó vacío.
   * - ``INVALID_NOMBRES_TYPE``
     - ``InvalidParameterError.Code.NOMBRES_TYPE``
     - 'nombres' no tiene el tipo de dato esperado.
   * - ``INVALID_NOMBRE_CONTRIBUYENTE_MISSING``
     - ``InvalidParameterError.Code.NOMBRE_CONTRIBUYENTE_MISSING``
     - Falta 'nombre_contribuyente' o llegó vacío.
   * - ``INVALID_NOMBRE_CONTRIBUYENTE_TYPE``
     - ``InvalidParameterError.Code.NOMBRE_CONTRIBUYENTE_TYPE``
     - 'nombre_contribuyente' no tiene el tipo de dato esperado.
   * - ``INVALID_NSS_MISSING``
     - ``InvalidParameterError.Code.NSS_MISSING``
     - Falta 'nss' o llegó vacío.
   * - ``INVALID_NSS_TYPE``
     - ``InvalidParameterError.Code.NSS_TYPE``
     - 'nss' no tiene el tipo de dato esperado.
   * - ``INVALID_NUMERO_SERIE_MISSING``
     - ``InvalidParameterError.Code.NUMERO_SERIE_MISSING``
     - Falta 'numero_serie' o llegó vacío.
   * - ``INVALID_NUMERO_SERIE_TYPE``
     - ``InvalidParameterError.Code.NUMERO_SERIE_TYPE``
     - 'numero_serie' no tiene el tipo de dato esperado.
   * - ``INVALID_NUMERO_SERIE_LENGTH``
     - ``InvalidParameterError.Code.NUMERO_SERIE_LENGTH``
     - La longitud o cantidad de 'numero_serie' está fuera de los límites.
   * - ``INVALID_NUMERO_SERIE_PLACAS_MISSING``
     - ``InvalidParameterError.Code.NUMERO_SERIE_PLACAS_MISSING``
     - Falta 'numero_serie_placas' o llegó vacío.
   * - ``INVALID_NUM_CREDITO_MISSING``
     - ``InvalidParameterError.Code.NUM_CREDITO_MISSING``
     - Falta 'num_credito' o llegó vacío.
   * - ``INVALID_OPTIONS_MISSING``
     - ``InvalidParameterError.Code.OPTIONS_MISSING``
     - Falta 'options' o llegó vacío.
   * - ``INVALID_OPTIONS_TYPE``
     - ``InvalidParameterError.Code.OPTIONS_TYPE``
     - 'options' no tiene el tipo de dato esperado.
   * - ``INVALID_OPTIONS_CORRELATION_ID_MISSING``
     - ``InvalidParameterError.Code.OPTIONS_CORRELATION_ID_MISSING``
     - Falta 'options_correlation_id' o llegó vacío.
   * - ``INVALID_OPTIONS_CORRELATION_ID_TYPE``
     - ``InvalidParameterError.Code.OPTIONS_CORRELATION_ID_TYPE``
     - 'options_correlation_id' no tiene el tipo de dato esperado.
   * - ``INVALID_OPTIONS_CORRELATION_ID_LENGTH``
     - ``InvalidParameterError.Code.OPTIONS_CORRELATION_ID_LENGTH``
     - La longitud o cantidad de 'options_correlation_id' está fuera de los límites.
   * - ``INVALID_OPTIONS_FILENAME_MISSING``
     - ``InvalidParameterError.Code.OPTIONS_FILENAME_MISSING``
     - Falta 'options_filename' o llegó vacío.
   * - ``INVALID_OPTIONS_FILENAME_TYPE``
     - ``InvalidParameterError.Code.OPTIONS_FILENAME_TYPE``
     - 'options_filename' no tiene el tipo de dato esperado.
   * - ``INVALID_OPTIONS_FILENAME_LENGTH``
     - ``InvalidParameterError.Code.OPTIONS_FILENAME_LENGTH``
     - La longitud o cantidad de 'options_filename' está fuera de los límites.
   * - ``INVALID_OPTIONS_METADATA_MISSING``
     - ``InvalidParameterError.Code.OPTIONS_METADATA_MISSING``
     - Falta 'options_metadata' o llegó vacío.
   * - ``INVALID_OPTIONS_METADATA_TYPE``
     - ``InvalidParameterError.Code.OPTIONS_METADATA_TYPE``
     - 'options_metadata' no tiene el tipo de dato esperado.
   * - ``INVALID_OPTIONS_TITLE_MISSING``
     - ``InvalidParameterError.Code.OPTIONS_TITLE_MISSING``
     - Falta 'options_title' o llegó vacío.
   * - ``INVALID_OPTIONS_TITLE_TYPE``
     - ``InvalidParameterError.Code.OPTIONS_TITLE_TYPE``
     - 'options_title' no tiene el tipo de dato esperado.
   * - ``INVALID_OPTIONS_TITLE_LENGTH``
     - ``InvalidParameterError.Code.OPTIONS_TITLE_LENGTH``
     - La longitud o cantidad de 'options_title' está fuera de los límites.
   * - ``INVALID_PAGE_MISSING``
     - ``InvalidParameterError.Code.PAGE_MISSING``
     - Falta 'page' o llegó vacío.
   * - ``INVALID_PAGE_TYPE``
     - ``InvalidParameterError.Code.PAGE_TYPE``
     - 'page' no tiene el tipo de dato esperado.
   * - ``INVALID_PAGE_RANGE``
     - ``InvalidParameterError.Code.PAGE_RANGE``
     - El valor de 'page' está fuera del rango permitido.
   * - ``INVALID_PAGE_SIZE_MISSING``
     - ``InvalidParameterError.Code.PAGE_SIZE_MISSING``
     - Falta 'page_size' o llegó vacío.
   * - ``INVALID_PAGE_SIZE_TYPE``
     - ``InvalidParameterError.Code.PAGE_SIZE_TYPE``
     - 'page_size' no tiene el tipo de dato esperado.
   * - ``INVALID_PAGE_SIZE_RANGE``
     - ``InvalidParameterError.Code.PAGE_SIZE_RANGE``
     - El valor de 'page_size' está fuera del rango permitido.
   * - ``INVALID_PASSWORD_MISSING``
     - ``InvalidParameterError.Code.PASSWORD_MISSING``
     - Falta 'password' o llegó vacío.
   * - ``INVALID_PASSWORD_TYPE``
     - ``InvalidParameterError.Code.PASSWORD_TYPE``
     - 'password' no tiene el tipo de dato esperado.
   * - ``INVALID_PATERNO_MISSING``
     - ``InvalidParameterError.Code.PATERNO_MISSING``
     - Falta 'paterno' o llegó vacío.
   * - ``INVALID_PATERNO_TYPE``
     - ``InvalidParameterError.Code.PATERNO_TYPE``
     - 'paterno' no tiene el tipo de dato esperado.
   * - ``INVALID_PERIODICIDAD_MISSING``
     - ``InvalidParameterError.Code.PERIODICIDAD_MISSING``
     - Falta 'periodicidad' o llegó vacío.
   * - ``INVALID_PERIODICIDAD_TYPE``
     - ``InvalidParameterError.Code.PERIODICIDAD_TYPE``
     - 'periodicidad' no tiene el tipo de dato esperado.
   * - ``INVALID_PERIODICIDAD_OPTION``
     - ``InvalidParameterError.Code.PERIODICIDAD_OPTION``
     - 'periodicidad' no está entre las opciones permitidas.
   * - ``INVALID_PERIODICIDAD_COMBINATION``
     - ``InvalidParameterError.Code.PERIODICIDAD_COMBINATION``
     - 'periodicidad' no es compatible con los demás parámetros.
   * - ``INVALID_PERIODO_MISSING``
     - ``InvalidParameterError.Code.PERIODO_MISSING``
     - Falta 'periodo' o llegó vacío.
   * - ``INVALID_PERIODO_TYPE``
     - ``InvalidParameterError.Code.PERIODO_TYPE``
     - 'periodo' no tiene el tipo de dato esperado.
   * - ``INVALID_PERIODO_LENGTH``
     - ``InvalidParameterError.Code.PERIODO_LENGTH``
     - La longitud o cantidad de 'periodo' está fuera de los límites.
   * - ``INVALID_PERIODO_RANGE``
     - ``InvalidParameterError.Code.PERIODO_RANGE``
     - El valor de 'periodo' está fuera del rango permitido.
   * - ``INVALID_PERIODO_FORMAT``
     - ``InvalidParameterError.Code.PERIODO_FORMAT``
     - 'periodo' no tiene el formato esperado.
   * - ``INVALID_PERIODO_OPTION``
     - ``InvalidParameterError.Code.PERIODO_OPTION``
     - 'periodo' no está entre las opciones permitidas.
   * - ``INVALID_PERMISSIONS_MISSING``
     - ``InvalidParameterError.Code.PERMISSIONS_MISSING``
     - Falta 'permissions' o llegó vacío.
   * - ``INVALID_PERMISSIONS_TYPE``
     - ``InvalidParameterError.Code.PERMISSIONS_TYPE``
     - 'permissions' no tiene el tipo de dato esperado.
   * - ``INVALID_PER_PAGE_MISSING``
     - ``InvalidParameterError.Code.PER_PAGE_MISSING``
     - Falta 'per_page' o llegó vacío.
   * - ``INVALID_PER_PAGE_TYPE``
     - ``InvalidParameterError.Code.PER_PAGE_TYPE``
     - 'per_page' no tiene el tipo de dato esperado.
   * - ``INVALID_PER_PAGE_RANGE``
     - ``InvalidParameterError.Code.PER_PAGE_RANGE``
     - El valor de 'per_page' está fuera del rango permitido.
   * - ``INVALID_PLACAS_MISSING``
     - ``InvalidParameterError.Code.PLACAS_MISSING``
     - Falta 'placas' o llegó vacío.
   * - ``INVALID_PLACAS_TYPE``
     - ``InvalidParameterError.Code.PLACAS_TYPE``
     - 'placas' no tiene el tipo de dato esperado.
   * - ``INVALID_PLACAS_LENGTH``
     - ``InvalidParameterError.Code.PLACAS_LENGTH``
     - La longitud o cantidad de 'placas' está fuera de los límites.
   * - ``INVALID_POSTAL_CODE_MISSING``
     - ``InvalidParameterError.Code.POSTAL_CODE_MISSING``
     - Falta 'postal_code' o llegó vacío.
   * - ``INVALID_POSTAL_CODE_TYPE``
     - ``InvalidParameterError.Code.POSTAL_CODE_TYPE``
     - 'postal_code' no tiene el tipo de dato esperado.
   * - ``INVALID_POSTAL_CODE_FORMAT``
     - ``InvalidParameterError.Code.POSTAL_CODE_FORMAT``
     - 'postal_code' no tiene el formato esperado.
   * - ``INVALID_POSTAL_CODE_MX_MISSING``
     - ``InvalidParameterError.Code.POSTAL_CODE_MX_MISSING``
     - Falta 'postal_code_mx' o llegó vacío.
   * - ``INVALID_POSTAL_CODE_MX_TYPE``
     - ``InvalidParameterError.Code.POSTAL_CODE_MX_TYPE``
     - 'postal_code_mx' no tiene el tipo de dato esperado.
   * - ``INVALID_POSTAL_CODE_MX_LENGTH``
     - ``InvalidParameterError.Code.POSTAL_CODE_MX_LENGTH``
     - La longitud o cantidad de 'postal_code_mx' está fuera de los límites.
   * - ``INVALID_POSTAL_CODE_MX_FORMAT``
     - ``InvalidParameterError.Code.POSTAL_CODE_MX_FORMAT``
     - 'postal_code_mx' no tiene el formato esperado.
   * - ``INVALID_PRIVATE_KEY_MISSING``
     - ``InvalidParameterError.Code.PRIVATE_KEY_MISSING``
     - Falta 'private_key' o llegó vacío.
   * - ``INVALID_PRIVATE_KEY_TYPE``
     - ``InvalidParameterError.Code.PRIVATE_KEY_TYPE``
     - 'private_key' no tiene el tipo de dato esperado.
   * - ``INVALID_REGIMEN_MISSING``
     - ``InvalidParameterError.Code.REGIMEN_MISSING``
     - Falta 'regimen' o llegó vacío.
   * - ``INVALID_REGIMEN_TYPE``
     - ``InvalidParameterError.Code.REGIMEN_TYPE``
     - 'regimen' no tiene el tipo de dato esperado.
   * - ``INVALID_REGIMEN_LENGTH``
     - ``InvalidParameterError.Code.REGIMEN_LENGTH``
     - La longitud o cantidad de 'regimen' está fuera de los límites.
   * - ``INVALID_REGIMEN_FISCAL_MISSING``
     - ``InvalidParameterError.Code.REGIMEN_FISCAL_MISSING``
     - Falta 'regimen_fiscal' o llegó vacío.
   * - ``INVALID_REGIMEN_FISCAL_TYPE``
     - ``InvalidParameterError.Code.REGIMEN_FISCAL_TYPE``
     - 'regimen_fiscal' no tiene el tipo de dato esperado.
   * - ``INVALID_REGIMEN_FISCAL_LENGTH``
     - ``InvalidParameterError.Code.REGIMEN_FISCAL_LENGTH``
     - La longitud o cantidad de 'regimen_fiscal' está fuera de los límites.
   * - ``INVALID_REGIMEN_FISCAL_FORMAT``
     - ``InvalidParameterError.Code.REGIMEN_FISCAL_FORMAT``
     - 'regimen_fiscal' no tiene el formato esperado.
   * - ``INVALID_RESET_TYPE``
     - ``InvalidParameterError.Code.RESET_TYPE``
     - 'reset' no tiene el tipo de dato esperado.
   * - ``INVALID_RESOURCE_MISSING``
     - ``InvalidParameterError.Code.RESOURCE_MISSING``
     - Falta 'resource' o llegó vacío.
   * - ``INVALID_RESOURCE_TYPE``
     - ``InvalidParameterError.Code.RESOURCE_TYPE``
     - 'resource' no tiene el tipo de dato esperado.
   * - ``INVALID_RESOURCE_PATH``
     - ``InvalidParameterError.Code.RESOURCE_PATH``
     - 'resource' forma parte de la URL y no puede ser '.' ni '..'.
   * - ``INVALID_RESOURCES_MISSING``
     - ``InvalidParameterError.Code.RESOURCES_MISSING``
     - Falta 'resources' o llegó vacío.
   * - ``INVALID_RESOURCES_TYPE``
     - ``InvalidParameterError.Code.RESOURCES_TYPE``
     - 'resources' no tiene el tipo de dato esperado.
   * - ``INVALID_RESOURCES_FIELD_MISSING``
     - ``InvalidParameterError.Code.RESOURCES_FIELD_MISSING``
     - Falta 'resources_field' o llegó vacío.
   * - ``INVALID_RESOURCES_FIELD_TYPE``
     - ``InvalidParameterError.Code.RESOURCES_FIELD_TYPE``
     - 'resources_field' no tiene el tipo de dato esperado.
   * - ``INVALID_RESOURCES_JSON_PATH_QUERY_MISSING``
     - ``InvalidParameterError.Code.RESOURCES_JSON_PATH_QUERY_MISSING``
     - Falta 'resources_json_path_query' o llegó vacío.
   * - ``INVALID_RESOURCES_JSON_PATH_QUERY_TYPE``
     - ``InvalidParameterError.Code.RESOURCES_JSON_PATH_QUERY_TYPE``
     - 'resources_json_path_query' no tiene el tipo de dato esperado.
   * - ``INVALID_RESOURCES_RESOURCE_MISSING``
     - ``InvalidParameterError.Code.RESOURCES_RESOURCE_MISSING``
     - Falta 'resources_resource' o llegó vacío.
   * - ``INVALID_RESOURCES_RESOURCE_TYPE``
     - ``InvalidParameterError.Code.RESOURCES_RESOURCE_TYPE``
     - 'resources_resource' no tiene el tipo de dato esperado.
   * - ``INVALID_RESOURCES_URL_MISSING``
     - ``InvalidParameterError.Code.RESOURCES_URL_MISSING``
     - Falta 'resources_url' o llegó vacío.
   * - ``INVALID_RESOURCES_URL_TYPE``
     - ``InvalidParameterError.Code.RESOURCES_URL_TYPE``
     - 'resources_url' no tiene el tipo de dato esperado.
   * - ``INVALID_REVERSO_MISSING``
     - ``InvalidParameterError.Code.REVERSO_MISSING``
     - Falta 'reverso' o llegó vacío.
   * - ``INVALID_REVERSO_TYPE``
     - ``InvalidParameterError.Code.REVERSO_TYPE``
     - 'reverso' no tiene el tipo de dato esperado.
   * - ``INVALID_RFC_MISSING``
     - ``InvalidParameterError.Code.RFC_MISSING``
     - Falta 'rfc' o llegó vacío.
   * - ``INVALID_RFC_TYPE``
     - ``InvalidParameterError.Code.RFC_TYPE``
     - 'rfc' no tiene el tipo de dato esperado.
   * - ``INVALID_RFC_NOMBRE_CONTRIBUYENTE_MISSING``
     - ``InvalidParameterError.Code.RFC_NOMBRE_CONTRIBUYENTE_MISSING``
     - Falta 'rfc_nombre_contribuyente' o llegó vacío.
   * - ``INVALID_ROW_ID_MISSING``
     - ``InvalidParameterError.Code.ROW_ID_MISSING``
     - Falta 'row_id' o llegó vacío.
   * - ``INVALID_ROW_ID_TYPE``
     - ``InvalidParameterError.Code.ROW_ID_TYPE``
     - 'row_id' no tiene el tipo de dato esperado.
   * - ``INVALID_ROW_ID_RANGE``
     - ``InvalidParameterError.Code.ROW_ID_RANGE``
     - El valor de 'row_id' está fuera del rango permitido.
   * - ``INVALID_SELECT_MISSING``
     - ``InvalidParameterError.Code.SELECT_MISSING``
     - Falta 'select' o llegó vacío.
   * - ``INVALID_SELECT_TYPE``
     - ``InvalidParameterError.Code.SELECT_TYPE``
     - 'select' no tiene el tipo de dato esperado.
   * - ``INVALID_SEXO_MISSING``
     - ``InvalidParameterError.Code.SEXO_MISSING``
     - Falta 'sexo' o llegó vacío.
   * - ``INVALID_SEXO_TYPE``
     - ``InvalidParameterError.Code.SEXO_TYPE``
     - 'sexo' no tiene el tipo de dato esperado.
   * - ``INVALID_SEXO_OPTION``
     - ``InvalidParameterError.Code.SEXO_OPTION``
     - 'sexo' no está entre las opciones permitidas.
   * - ``INVALID_SORT_MISSING``
     - ``InvalidParameterError.Code.SORT_MISSING``
     - Falta 'sort' o llegó vacío.
   * - ``INVALID_SORT_TYPE``
     - ``InvalidParameterError.Code.SORT_TYPE``
     - 'sort' no tiene el tipo de dato esperado.
   * - ``INVALID_TEMPLATE_MISSING``
     - ``InvalidParameterError.Code.TEMPLATE_MISSING``
     - Falta 'template' o llegó vacío.
   * - ``INVALID_TEMPLATE_TYPE``
     - ``InvalidParameterError.Code.TEMPLATE_TYPE``
     - 'template' no tiene el tipo de dato esperado.
   * - ``INVALID_TEMPLATE_ID_MISSING``
     - ``InvalidParameterError.Code.TEMPLATE_ID_MISSING``
     - Falta 'template_id' o llegó vacío.
   * - ``INVALID_TEMPLATE_ID_TYPE``
     - ``InvalidParameterError.Code.TEMPLATE_ID_TYPE``
     - 'template_id' no tiene el tipo de dato esperado.
   * - ``INVALID_TEMPLATE_ID_PATH``
     - ``InvalidParameterError.Code.TEMPLATE_ID_PATH``
     - 'template_id' forma parte de la URL y no puede ser '.' ni '..'.
   * - ``INVALID_TIPO_COMPROBANTE_MISSING``
     - ``InvalidParameterError.Code.TIPO_COMPROBANTE_MISSING``
     - Falta 'tipo_comprobante' o llegó vacío.
   * - ``INVALID_TIPO_COMPROBANTE_TYPE``
     - ``InvalidParameterError.Code.TIPO_COMPROBANTE_TYPE``
     - 'tipo_comprobante' no tiene el tipo de dato esperado.
   * - ``INVALID_TIPO_COMPROBANTE_OPTION``
     - ``InvalidParameterError.Code.TIPO_COMPROBANTE_OPTION``
     - 'tipo_comprobante' no está entre las opciones permitidas.
   * - ``INVALID_TRANSACTION_ID_MISSING``
     - ``InvalidParameterError.Code.TRANSACTION_ID_MISSING``
     - Falta 'transaction_id' o llegó vacío.
   * - ``INVALID_TRANSACTION_ID_TYPE``
     - ``InvalidParameterError.Code.TRANSACTION_ID_TYPE``
     - 'transaction_id' no tiene el tipo de dato esperado.
   * - ``INVALID_TRANSACTION_ID_RANGE``
     - ``InvalidParameterError.Code.TRANSACTION_ID_RANGE``
     - El valor de 'transaction_id' está fuera del rango permitido.
   * - ``INVALID_USO_CFDI_MISSING``
     - ``InvalidParameterError.Code.USO_CFDI_MISSING``
     - Falta 'uso_cfdi' o llegó vacío.
   * - ``INVALID_USO_CFDI_TYPE``
     - ``InvalidParameterError.Code.USO_CFDI_TYPE``
     - 'uso_cfdi' no tiene el tipo de dato esperado.
   * - ``INVALID_USO_CFDI_LENGTH``
     - ``InvalidParameterError.Code.USO_CFDI_LENGTH``
     - La longitud o cantidad de 'uso_cfdi' está fuera de los límites.
   * - ``INVALID_UUID_MISSING``
     - ``InvalidParameterError.Code.UUID_MISSING``
     - Falta 'uuid' o llegó vacío.
   * - ``INVALID_UUID_TYPE``
     - ``InvalidParameterError.Code.UUID_TYPE``
     - 'uuid' no tiene el tipo de dato esperado.
   * - ``INVALID_UUID_FORMAT``
     - ``InvalidParameterError.Code.UUID_FORMAT``
     - 'uuid' no tiene el formato esperado.
   * - ``INVALID_UUID_PATH``
     - ``InvalidParameterError.Code.UUID_PATH``
     - 'uuid' forma parte de la URL y no puede ser '.' ni '..'.
   * - ``INVALID_WAIT_TYPE``
     - ``InvalidParameterError.Code.WAIT_TYPE``
     - 'wait' no tiene el tipo de dato esperado.
   * - ``INVALID_WEBHOOK_MISSING``
     - ``InvalidParameterError.Code.WEBHOOK_MISSING``
     - Falta 'webhook' o llegó vacío.
   * - ``INVALID_WEBHOOK_TYPE``
     - ``InvalidParameterError.Code.WEBHOOK_TYPE``
     - 'webhook' no tiene el tipo de dato esperado.
   * - ``INVALID_WEBHOOK_FORMAT``
     - ``InvalidParameterError.Code.WEBHOOK_FORMAT``
     - 'webhook' no tiene el formato esperado.
   * - ``INVALID_YEAR_MISSING``
     - ``InvalidParameterError.Code.YEAR_MISSING``
     - Falta 'year' o llegó vacío.
   * - ``INVALID_YEAR_TYPE``
     - ``InvalidParameterError.Code.YEAR_TYPE``
     - 'year' no tiene el tipo de dato esperado.
   * - ``INVALID_YEAR_RANGE``
     - ``InvalidParameterError.Code.YEAR_RANGE``
     - El valor de 'year' está fuera del rango permitido.

----

Archivos — ``InvalidFileError``
-------------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 34 38

   * - Código
     - Miembro del Enum
     - Descripción
   * - ``INVALID_ANVERSO_FILE_NOT_FOUND``
     - ``InvalidFileError.Code.ANVERSO_FILE_NOT_FOUND``
     - No existe el archivo indicado en 'anverso'.
   * - ``INVALID_ANVERSO_FILE_UNREADABLE``
     - ``InvalidFileError.Code.ANVERSO_FILE_UNREADABLE``
     - No se puede leer el archivo de 'anverso'.
   * - ``INVALID_ANVERSO_FILE_EMPTY``
     - ``InvalidFileError.Code.ANVERSO_FILE_EMPTY``
     - El archivo de 'anverso' está vacío.
   * - ``INVALID_ANVERSO_FILE_TYPE``
     - ``InvalidFileError.Code.ANVERSO_FILE_TYPE``
     - El tipo del archivo de 'anverso' no está permitido.
   * - ``INVALID_ANVERSO_FILE_SIZE``
     - ``InvalidFileError.Code.ANVERSO_FILE_SIZE``
     - El archivo de 'anverso' supera el tamaño máximo.
   * - ``INVALID_CERTIFICATE_FILE_NOT_FOUND``
     - ``InvalidFileError.Code.CERTIFICATE_FILE_NOT_FOUND``
     - No existe el archivo indicado en 'certificate'.
   * - ``INVALID_CERTIFICATE_FILE_UNREADABLE``
     - ``InvalidFileError.Code.CERTIFICATE_FILE_UNREADABLE``
     - No se puede leer el archivo de 'certificate'.
   * - ``INVALID_CERTIFICATE_FILE_EMPTY``
     - ``InvalidFileError.Code.CERTIFICATE_FILE_EMPTY``
     - El archivo de 'certificate' está vacío.
   * - ``INVALID_CSF_FILE_NOT_FOUND``
     - ``InvalidFileError.Code.CSF_FILE_NOT_FOUND``
     - No existe el archivo indicado en 'csf'.
   * - ``INVALID_CSF_FILE_UNREADABLE``
     - ``InvalidFileError.Code.CSF_FILE_UNREADABLE``
     - No se puede leer el archivo de 'csf'.
   * - ``INVALID_CSF_FILE_EMPTY``
     - ``InvalidFileError.Code.CSF_FILE_EMPTY``
     - El archivo de 'csf' está vacío.
   * - ``INVALID_CSF_FILE_TYPE``
     - ``InvalidFileError.Code.CSF_FILE_TYPE``
     - El tipo del archivo de 'csf' no está permitido.
   * - ``INVALID_DATA_FILE_NOT_FOUND``
     - ``InvalidFileError.Code.DATA_FILE_NOT_FOUND``
     - No existe el archivo indicado en 'data'.
   * - ``INVALID_DATA_FILE_UNREADABLE``
     - ``InvalidFileError.Code.DATA_FILE_UNREADABLE``
     - No se puede leer el archivo de 'data'.
   * - ``INVALID_DATA_FILE_EMPTY``
     - ``InvalidFileError.Code.DATA_FILE_EMPTY``
     - El archivo de 'data' está vacío.
   * - ``INVALID_DATA_FILE_TYPE``
     - ``InvalidFileError.Code.DATA_FILE_TYPE``
     - El tipo del archivo de 'data' no está permitido.
   * - ``INVALID_PRIVATE_KEY_FILE_NOT_FOUND``
     - ``InvalidFileError.Code.PRIVATE_KEY_FILE_NOT_FOUND``
     - No existe el archivo indicado en 'private_key'.
   * - ``INVALID_PRIVATE_KEY_FILE_UNREADABLE``
     - ``InvalidFileError.Code.PRIVATE_KEY_FILE_UNREADABLE``
     - No se puede leer el archivo de 'private_key'.
   * - ``INVALID_PRIVATE_KEY_FILE_EMPTY``
     - ``InvalidFileError.Code.PRIVATE_KEY_FILE_EMPTY``
     - El archivo de 'private_key' está vacío.
   * - ``INVALID_REVERSO_FILE_NOT_FOUND``
     - ``InvalidFileError.Code.REVERSO_FILE_NOT_FOUND``
     - No existe el archivo indicado en 'reverso'.
   * - ``INVALID_REVERSO_FILE_UNREADABLE``
     - ``InvalidFileError.Code.REVERSO_FILE_UNREADABLE``
     - No se puede leer el archivo de 'reverso'.
   * - ``INVALID_REVERSO_FILE_EMPTY``
     - ``InvalidFileError.Code.REVERSO_FILE_EMPTY``
     - El archivo de 'reverso' está vacío.
   * - ``INVALID_REVERSO_FILE_TYPE``
     - ``InvalidFileError.Code.REVERSO_FILE_TYPE``
     - El tipo del archivo de 'reverso' no está permitido.
   * - ``INVALID_REVERSO_FILE_SIZE``
     - ``InvalidFileError.Code.REVERSO_FILE_SIZE``
     - El archivo de 'reverso' supera el tamaño máximo.
   * - ``INVALID_TEMPLATE_FILE_NOT_FOUND``
     - ``InvalidFileError.Code.TEMPLATE_FILE_NOT_FOUND``
     - No existe el archivo indicado en 'template'.
   * - ``INVALID_TEMPLATE_FILE_UNREADABLE``
     - ``InvalidFileError.Code.TEMPLATE_FILE_UNREADABLE``
     - No se puede leer el archivo de 'template'.
   * - ``INVALID_TEMPLATE_FILE_EMPTY``
     - ``InvalidFileError.Code.TEMPLATE_FILE_EMPTY``
     - El archivo de 'template' está vacío.
   * - ``INVALID_TEMPLATE_FILE_SIZE``
     - ``InvalidFileError.Code.TEMPLATE_FILE_SIZE``
     - El archivo de 'template' supera el tamaño máximo.
   * - ``INVALID_TEMPLATE_FILE_CONTENT``
     - ``InvalidFileError.Code.TEMPLATE_FILE_CONTENT``
     - El contenido del archivo de 'template' no es válido.

----

Configuración — ``ConfigurationError``
--------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 34 38

   * - Código
     - Miembro del Enum
     - Descripción
   * - ``CONFIG_API_KEY_MISSING``
     - ``ConfigurationError.Code.API_KEY_MISSING``
     - No se configuró la llave de API Market.
   * - ``CONFIG_IDSE_CREDENTIALS_MISSING``
     - ``ConfigurationError.Code.IDSE_CREDENTIALS_MISSING``
     - No se configuraron las credenciales de IDSE Pro.

----

Respuestas de la API — ``APIError``
-----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 34 38

   * - Código
     - Miembro del Enum
     - Descripción
   * - ``API_REQUEST_INVALID``
     - ``ErrorCode.API_REQUEST_INVALID``
     - HTTP 400: la API rechazó la solicitud.
   * - ``API_KEY_UNAUTHORIZED``
     - ``ErrorCode.API_KEY_UNAUTHORIZED``
     - HTTP 401: la llave no es válida.
   * - ``API_PAYMENT_REQUIRED``
     - ``ErrorCode.API_PAYMENT_REQUIRED``
     - HTTP 402: se requiere saldo o un paquete superior.
   * - ``API_PERMISSION_FORBIDDEN``
     - ``ErrorCode.API_PERMISSION_FORBIDDEN``
     - HTTP 403: la llave no tiene permiso para el servicio.
   * - ``API_RESOURCE_NOT_FOUND``
     - ``ErrorCode.API_RESOURCE_NOT_FOUND``
     - HTTP 404: no se encontró el recurso.
   * - ``API_REQUEST_UNPROCESSABLE``
     - ``ErrorCode.API_REQUEST_UNPROCESSABLE``
     - HTTP 422: la API no aceptó los datos.
   * - ``API_REQUEST_LIMIT_EXCEEDED``
     - ``ErrorCode.API_REQUEST_LIMIT_EXCEEDED``
     - HTTP 429: demasiadas solicitudes.
   * - ``API_REQUEST_FAILED``
     - ``ErrorCode.API_REQUEST_FAILED``
     - Otro error HTTP 4xx.
   * - ``API_SERVER_ERROR``
     - ``ErrorCode.API_SERVER_ERROR``
     - Error HTTP 5xx.
   * - ``API_SERVICE_UNAVAILABLE``
     - ``ErrorCode.API_SERVICE_UNAVAILABLE``
     - HTTP 502, 503 o 504: el servicio no está disponible.
   * - ``API_RESPONSE_INVALID``
     - ``ErrorCode.API_RESPONSE_INVALID``
     - La API respondió algo que no se puede interpretar.

----

Red — ``httpx.HTTPError``
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 34 38

   * - Código
     - Miembro del Enum
     - Descripción
   * - ``NETWORK_CONNECTION_ERROR``
     - ``ErrorCode.NETWORK_CONNECTION_ERROR``
     - No fue posible conectar con la API.
   * - ``NETWORK_RESPONSE_TIMEOUT``
     - ``ErrorCode.NETWORK_RESPONSE_TIMEOUT``
     - La API no respondió a tiempo.

----

Línea de comandos — ``CLI``
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 34 38

   * - Código
     - Miembro del Enum
     - Descripción
   * - ``CLI_ARGUMENTS_INVALID``
     - ``ErrorCode.CLI_ARGUMENTS_INVALID``
     - Faltan argumentos o tienen un tipo incorrecto.

----

Errores de la API
-----------------

Además de ``code``, los errores de la API exponen:

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Atributo
     - Contenido
   * - ``message``
     - Mensaje de la API.
   * - ``status``
     - Estado indicado en el cuerpo de la respuesta.
   * - ``success``
     - Indicador de éxito del cuerpo.
   * - ``codigo_validacion``
     - Código de la solicitud; inclúyalo al pedir soporte.
   * - ``additional_data``
     - Campos sin atributo propio.
   * - ``response_status_code``
     - Código HTTP.

Los servicios por grupo lanzan ``apimarket.ApiMarketError``, que además expone ``data`` y ``body``. Los demás
lanzan una clase tipada por endpoint y código, como ``LocalizarUmf401Error``. Si la respuesta de error no es JSON,
los atributos tomados del cuerpo quedan en ``None``.

La API puede responder HTTP 200 con un ``status`` de falla en el cuerpo. Con un ``status`` 500 o mayor, los
servicios por grupo lanzan ``ApiMarketError`` y todos los comandos de la CLI terminan con error. Las funciones
anteriores de Python devuelven la respuesta sin lanzar excepción: revise ``status``.

----

Ejemplos de uso
---------------

Capturar cualquier error del SDK:

.. code-block:: python

   import apimarket
   import httpx
   from kiota_abstractions.api_error import APIError

   try:
       apimarket.get_assigned_umf(nss)
   except apimarket.ValidationError as e:      # no se envió nada
       print(e.code.value, e.message)
   except APIError as e:                       # respondió la API
       print(e.code.value, e.status, e.codigo_validacion, e.message)
   except httpx.HTTPError as e:                # red
       print(e.code.value, e.message)

Capturar y leer el código de error:

.. code-block:: python

   from apimarket.validations import validate_curp, InvalidCURPError

   try:
       validate_curp("INVALIDO")
   except InvalidCURPError as e:
       print(e.code.value)   # "INVALID_CURP_LENGTH"
       print(e.message)      # "Longitud inválida: se esperaban 18 caracteres, se recibieron 8."
       print(str(e))         # "[INVALID_CURP_LENGTH] CURP: INVALIDO - Longitud inválida..."

Comparar el código para manejar cada caso:

.. code-block:: python

   from apimarket.validations import validate_curp, InvalidCURPError

   try:
       validate_curp(curp)
   except InvalidCURPError as e:
       if e.code == InvalidCURPError.Code.INVALID_LENGTH:
           print("El CURP debe tener 18 caracteres.")
       elif e.code == InvalidCURPError.Code.INVALID_FORMAT:
           print("El formato del CURP no es válido.")
       elif e.code == InvalidCURPError.Code.INVALID_DIGIT:
           print(f"Dígito verificador incorrecto: {e.message}")

El mismo patrón aplica para ``InvalidRFCError`` e ``InvalidNSSError``:

.. code-block:: python

   from apimarket.validations import validate_rfc, InvalidRFCError
   from apimarket.validations import validate_nss, InvalidNSSError

   try:
       validate_rfc(rfc)
   except InvalidRFCError as e:
       if e.code == InvalidRFCError.Code.INVALID_FORMAT:
           print("El RFC no tiene el formato correcto.")

   try:
       validate_nss(nss)
   except InvalidNSSError as e:
       if e.code == InvalidNSSError.Code.INVALID_DIGIT:
           print("El dígito verificador del NSS es incorrecto.")
