import pytest
from starlette.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="module")
def test_note_oid():
    return "6260537e600a744e22523260"


@pytest.fixture(scope="module")
def test_note():
    return {
        "title": "title_data",
        "body": "text_data",
        "created": "2022-04-25T13:20:29.768000+00:00",
        "modified": "2022-04-25T13:20:29.768000+00:00",
    }


@pytest.fixture(scope="module")
def test_note_db():
    return {
        "note_id": "6260537e600a744e22523260",
        "title": "title_data",
        "body": "text_data",
        "created": "2022-04-25T13:20:29.768000+00:00",
        "modified": "2022-04-25T13:20:29.768000+00:00",
    }


@pytest.fixture(scope="module")
def test_note_db_1():
    return {
        "note_id": "6260537e600a744e22523262",
        "title": "title_data1",
        "body": "text_data2",
        "created": "2022-04-25T13:20:29.768000+00:00",
        "modified": "2022-04-25T13:20:29.768000+00:00",
    }


@pytest.fixture(scope="module")
def test_template_oid():
    return "6260537e600a744e22523264"


@pytest.fixture(scope="module")
def test_template():
    return {
        "title": "template_data",
        "body": "template_body",
    }


@pytest.fixture(scope="module")
def test_template_db():
    return {
        "template_id": "6260537e600a744e22523264",
        "title": "template_data",
        "body": "template_body",
    }


@pytest.fixture(scope="module")
def test_template_db_1():
    return {
        "template_id": "6260537e600a744e22523266",
        "title": "template_data",
        "body": "template_body",
    }
