=========
Changelog
=========

Sin publicar
============

- Ayuda de la CLI rediseñada: todos los comandos por área, ayuda por área y por comando con ejemplo y códigos
  de error, mensajes en español y sugerencias ante errores de escritura. ``apimarket`` sin argumentos la muestra.
- 61 servicios nuevos disponibles en Python y en la CLI (``apimarket GRUPO SERVICIO``).
- ``ApiMarketError`` expone ``status``, ``success``, ``codigo_validacion``, ``data`` y ``additional_data``,
  como los errores tipados.
- Todas las funciones validan sus parámetros antes de llamar a la API; base común ``ValidationError``.
- Todos los errores llevan ``code``, incluidos los de la API y de red; catálogo en ``apimarket errores``.
- CAMBIO: las fechas de nacimiento deben tener exactamente 2, 2 y 4 dígitos.
- CAMBIO: la CLI muestra ``Error [CÓDIGO]: mensaje``; en modo asíncrono las funciones devuelven una corrutina
  que agrega ``code`` a los errores.
- CAMBIO: sin llave configurada se lanza ``CONFIG_API_KEY_MISSING`` sin enviar la petición.
- Todas las funciones validan sus parámetros antes de llamar a la API; base común ``ValidationError``.
- Todos los errores llevan ``code``, incluidos los de la API y de red; catálogo en ``apimarket errores``.
- CAMBIO: las fechas de nacimiento deben tener exactamente 2, 2 y 4 dígitos.
- CAMBIO: la CLI muestra ``Error [CÓDIGO]: mensaje``; en modo asíncrono las funciones devuelven una corrutina
  que agrega ``code`` a los errores.
- CAMBIO: sin llave configurada se lanza ``CONFIG_API_KEY_MISSING`` sin enviar la petición.
- Nueva ``InvalidCreditError`` (``INVALID_CREDIT_FORMAT``) para el número de crédito INFONAVIT.
- Nuevas ``InvalidParameterError`` e ``InvalidFileError`` con un código por campo
  (``INVALID_<CAMPO>_<MOTIVO>``); heredan de ``ValueError``. Los códigos de API, red, configuración y CLI usan
  el origen como prefijo.
- FIX: ``store_token()`` y ``verify_sat_signature()`` fallaban siempre; ahora envían el cuerpo de la petición.
  Ambas devuelven un ``dict``.
- FIX: en modo síncrono, la segunda llamada fallaba con ``Event loop is closed``.
- FIX: las llamadas simultáneas (``asyncio.gather`` o varios hilos) podían enviar los parámetros de otra llamada.
- FIX: se declara la dependencia ``sniffio`` requerida en Python 3.14.
- FIX: los comandos cortos (``-vc``, ``-bn``...) mostraban un volcado ante un error de la API o de conexión;
  ahora muestran la respuesta y el mensaje, y salen con código 1.

Version 0.1
===========

- Feature A added
- FIX: nasty bug #1729 fixed
- add your changes here!
