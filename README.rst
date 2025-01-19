.. image:: https://img.shields.io/pypi/v/apimarket.svg
   :alt: PyPI-Server
   :target: https://pypi.org/project/apimarket/

.. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
   :alt: Twitter
   :target: https://twitter.com/apimarketmx

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
   :alt: Project generated with PyScaffold
   :target: https://pyscaffold.org/


=========
apimarket
=========

This SDK is an open-source development project that enables you to connect to ApiMarket services using Python.

Benefits
    Algorithm-based verifications.
    Exponential retry mechanism.
    Transparent saving to your backend, with default caching on your file system.
    Typing support for seamless use in your IDE.



Installation
------------

.. code-block:: bash

   pip install apimarket

   
Getting Started
-------

1. Copy a token in https://apimarket.mx/app/tokens

2. Choose the service you need https://apimarket.mx/marketplace and select the Python SDK

3. Test your code
.. code-block:: python3

   import apimarket
   # Copy the token from https://apimarket.mx/app/tokens
   # You only need to configure the Token once.
   apimarket.assemble(api_key="A7ee6195-4ff1-4ed2-bdf9-b950863fX3b9", sandbox=False)
   # Choose the service you need https://apimarket.mx/marketplace
   curp_details = apimarket.fetch_curp_details("LOOA531113HTCPBN07")
   print(curp_details)



Save API KEY securily
------------
There are three different ways to set the API key: you can set the API key as an environment variable in your shell, in the .env file, or call functions with your API key.

.. code-block:: bash

   export APIMARKET_API_KEY="REPLACE-WITH-YOUR-API-HERE"

.. code-block:: bash

   APIMARKET_API_KEY="REPLACE-WITH-YOUR-API-HERE"


Usage
------------
Learn how to install and use the program through this `playground <./notebooks/playground.ipynb>`_.


Python
-------
You can consult the full list on Python Docs.

Fetch CURP details
++++++++++++++++++

.. code-block:: python3

   import apimarket
   # You can configure the calls with apimarket.assemble(api_key: str, async_client:boolean=False, headers:dict[str,str], sandbox=False)
   result = apimarket.fetch_curp_details("LOOA531113HTCPBN07")
   print(result)

   
Fetch "Historial Laboral" details
++++++++++++++++++

.. code-block:: python3

   import apimarket
   # You can configure the calls with apimarket.assemble(api_key: str, async_client:boolean=False, headers:dict[str,str], sandbox=False)
   result = apimarket.get_labor_history("CURP", "NSS")
   print(result)


Multiple calls
++++++++++++++++++

.. code-block:: python3

   import apimarket
   # You can configure the calls with apimarket.assemble(api_key: str, async_client:boolean=False, headers:dict[str,str], sandbox=False)
   apimarket.assemble(api_key="A7ee6195-4ff1-4ed2-bdf9-b950863fX3b9", sandbox=False)
   CURP = ""
   NSS= ""
   curp_details = apimarket.fetch_curp_details(CURP, NSS)
   labor_history = apimarket.get_labor_history(CURP, NSS)
   print(result)


CLI
----
You can consult the full list on CLI Docs.

Fetch CURP details
+++++++++++++++++++


.. code-block:: bash

   apimarket -c LOOA531113HTCPBN07

Combine different requests
+++++++++++++++++++++++++++


.. code-block:: bash

   apimarket -c LOOA531113HTCPBN07 --get-rfc-from-curp LOOA531113HTCPBN07  | jq -s 'add'


Read a CSV with your customs fields
++++++++++++++++++++++++++++++++++++

csvcut belongs to csvkit library

.. code-block:: bash

   csvcut apimarket-consulta.csv -c 'CURP' | xargs -P 8 -I {} apimarket -c {} 2>"error.txt" | jq -s > curps.json


.. _pyscaffold-notes:


Servicios (Español)
-----------

Valida CURP API
++++++++++++++++++++++++++++++++++++

Valida CURP API, es una API REST para la obtención y validación de los registros de nacimiento relacionados a la Clave Única de Registro de Población (CURP) en el Registro Nacional de Población (RENAPO) localizados en México en formato JSON. Este endpoint no usa un algoritmo, sino que consulta las fuentes oficiales. Este servicio cumple con la normativa de nuestra parte, te recomendamos leer nuestros nuestros términos y condiciones.
Más información en https://apimarket.mx/marketplace/valida-curp


Historial Laboral IMSS API
++++++++++++++++++++++++++++++++++++

Historial Laboral IMSS API, es una API REST para la obtención del historial Laboral registrado en el IMSS con sus semanas cotizadas, fechas de alta y baja, asi como el salario, razón social y registro patronal del empleador localizados en México en formato JSON. Este endpoint no usa un algoritmo, sino que consulta las fuentes oficiales. Más información en https://apimarket.mx/marketplace/consultar-historial-laboral




Dudas y opiniones
-------------------

Correo
++++++++++++++++++++++++++++++++++++

Mediante correo electrónico: soporte@apimarket.mx
WhatsApp: https://api.whatsapp.com/message/CEUT72XQ5FKGP1

