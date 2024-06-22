import pytest

import apimarket

__author__ = "Carlos Eduardo Sanchez Torres (sanchezcarlosjr)"
__copyright__ = "Carlos Eduardo Sanchez Torres (sanchezcarlosjr)"
__license__ = "MIT"

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_async_fetch_curp_details():
    apimarket.assemble(async_client=True)
    response = await apimarket.fetch_curp_details("LOOA531113HTCPBN07")
    assert response.data.apellido_paterno == 'LOPEZ'
    assert response.data.apellido_materno == 'OBRADOR'


def test_sync_fetch_curp_details():
    apimarket.assemble(async_client=False)
    response = apimarket.fetch_curp_details("LOOA531113HTCPBN07")
    assert response.data.apellido_paterno == 'LOPEZ'
    assert response.data.apellido_materno == 'OBRADOR'
