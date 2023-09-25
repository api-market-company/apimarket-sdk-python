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

API Market Python Open Source Development

Installation
------------

.. code-block:: bash

   pip install apimarket

Set API KEY
------------
There are three different ways to set the API key: you can set the API key as an environment variable in your shell, in the .env file, or call functions with your API key.

.. code-block:: bash

   export APIMARKET_API_KEY="REPLACE-WITH-YOUR-API-HERE"

.. code-block:: bash

   APIMARKET_API_KEY="REPLACE-WITH-YOUR-API-HERE"


Python
-------

Fetch CURP details
++++++++++++++++++

.. code-block:: python3

   import apimarket
   # Also it is possible apimarket.fetch_curp_details("LOOA531113HTCPBN07", api_key="")
   result = apimarket.fetch_curp_details("LOOA531113HTCPBN07") 
   print(result)

CLI
----

Fetch CURP details
+++++++++++++++++++


.. code-block:: bash

   apimarket -c LOOA531113HTCPBN07

Combine different requests
+++++++++++++++++++++++++++


.. code-block:: bash

   apimarket -c LOOA531113HTCPBN07 --get-rfc-from-curp LOOA531113HTCPBN07  | jq -s 'add'


.. _pyscaffold-notes:

Note
----

This project has been set up using PyScaffold 4.5. For details and usage information on PyScaffold see https://pyscaffold.org/.
