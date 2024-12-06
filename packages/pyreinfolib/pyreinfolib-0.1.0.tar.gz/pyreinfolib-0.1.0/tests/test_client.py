from dataclasses import dataclass
import pytest
from unittest.mock import patch

from pyreinfolib import Client

@dataclass
class GetMunicipalitiesArgs:
    area: int
    language: str

@dataclass
class GetMunicipalitiesTestCase:
    args: GetMunicipalitiesArgs
    expected: dict
    error: Exception | None

@pytest.mark.parametrize(
    ["test_case"],
    [
        pytest.param(
            GetMunicipalitiesTestCase(
                args=GetMunicipalitiesArgs(
                    area=13,
                    language="ja",
                ),
                expected={"status": "OK", "data": [{"id": "13101", "name": "千代田区"}]},
                error=None,
            ),
            id="normal"
        )
    ]
)
@patch('pyreinfolib.Client')
def get_municipalities():
    client = Client(api_key="dummy")


