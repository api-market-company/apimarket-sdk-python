.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/apimarket.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/apimarket
    .. image:: https://readthedocs.org/projects/apimarket/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://apimarket.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/apimarket/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/apimarket
    .. image:: https://img.shields.io/pypi/v/apimarket.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/apimarket/
    .. image:: https://img.shields.io/conda/vn/conda-forge/apimarket.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/apimarket
    .. image:: https://pepy.tech/badge/apimarket/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/apimarket
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/apimarket

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

=========
API MARKET
=========


    
    API Market Python Open Source Development


Installation
=========
.. code-block:: bash

   pip install apimarket


Fetch CURP details
=========
.. code-block:: python3

   import apimarket
   result = apimarket.fetch_curp_details("LOOA531113HTCPBN07", api_key="")
   print(result)

    



CLI
=========

.. code-block:: bash

   apimarket -c LOOA531113HTCPBN07
   



.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
