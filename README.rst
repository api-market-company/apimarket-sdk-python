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

Fetch CURP details
------------------

.. code-block:: python3

   import apimarket
   result = apimarket.fetch_curp_details("LOOA531113HTCPBN07", api_key="")
   print(result)

CLI
---

.. code-block:: bash

   apimarket -c LOOA531113HTCPBN07

.. _pyscaffold-notes:

Note
----

This project has been set up using PyScaffold 4.5. For details and usage information on PyScaffold see https://pyscaffold.org/.
