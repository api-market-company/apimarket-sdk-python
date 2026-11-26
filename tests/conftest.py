import threading

import pytest
import apimarket
from support import Server, connect


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture
def sdk():
    apimarket.assemble(async_client=False)


@pytest.fixture
def sdk_async():
    apimarket.assemble(async_client=True)


@pytest.fixture
def sdk_sandbox():
    """SDK síncrono en modo sandbox, sin importar lo que diga el entorno."""
    apimarket.assemble(sandbox=True, headers={"x-sandbox": "true"})
    yield
    apimarket.assemble()


@pytest.fixture
def server():
    """Servidor local que registra las peticiones; no usa la red ni la llave real."""
    instance = Server()
    threading.Thread(target=instance.serve_forever, args=(0.01,), daemon=True).start()
    connect(instance)
    yield instance
    instance.shutdown()
    instance.server_close()
    apimarket.assemble()
