import pytest
from starlette.testclient import TestClient

from app.config import get_config
from app.database import db, get_database
from app.main import app


config = get_config()


@pytest.fixture(scope="module")
async def database(db_path, db_name):
    await db.connect_to_database(path=config.db_path, name=config.db_name)
    return await get_database()


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="module")
def test_oid():
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
