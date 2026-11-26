"""Cada código del catálogo se produce con un caso real, con su mensaje y sus campos."""
import pytest
from kiota_abstractions.api_error import APIError

import apimarket
from apimarket.errors import CATALOG, ErrorCode
from apimarket.validations import ValidationError

from error_scenarios import SCENARIOS


def test_every_code_has_a_scenario():
    expected = [code for _, _, codes in CATALOG for code, _ in codes]
    assert sorted(s.code.value for s in SCENARIOS) == sorted(code.value for code in expected)


@pytest.mark.parametrize("scenario", SCENARIOS, ids=[s.code.value for s in SCENARIOS])
def test_scenario_produces_its_code(server, scenario):
    scenario.setup(server)
    with pytest.raises(Exception) as exc_info:
        scenario.call()
    error = exc_info.value
    assert error.code is scenario.code
    assert getattr(error, "message", None) or str(error)
    assert bool(server.requests) is scenario.sends_request
    if not isinstance(scenario.code, ErrorCode):
        assert isinstance(error, (ValidationError, ValueError))
    if isinstance(error, APIError) and scenario.code is not ErrorCode.API_RESPONSE_INVALID:
        assert isinstance(error, apimarket.ApiMarketError)
        assert error.success is False
        assert error.codigo_validacion == "EJEMPLO123"
        assert error.status == error.response_status_code
