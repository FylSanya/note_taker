import pytest
from starlette.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


@pytest.fixture()
def test_oid():
    return "6260537e600a744e22523260"


@pytest.fixture()
def test_payload1():
    return {
        "title": {"text": "string"},
        "text": {"text": "string"},
        "tags": ["string"],
        "checklist_items": [{"text": "string", "is_checked": True}],
        "list_items": [{"text": "string"}],
    }
