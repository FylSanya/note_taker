import json


def test_add_note(test_app, monkeypatch, test_note):
    async def mock_note(self, payload):
        return None

    monkeypatch.setattr("app.database.MongoManager.add_note", mock_note)
    response = test_app.post("/notes/", data=json.dumps(test_note))

    assert response.status_code == 201
    assert response.json() is None


def test_add_note_invalid_json(test_app):
    response = test_app.post("/notes/", data=json.dumps({"title": "something"}))
    assert response.status_code == 422


def test_get_note(test_app, monkeypatch, test_note_db, test_oid):
    async def mock_get(self, note_id):
        return test_note_db

    monkeypatch.setattr("app.database.MongoManager.get_note", mock_get)

    response = test_app.get(f"/notes/{test_oid}")
    assert response.status_code == 200
    assert response.json() == test_note_db


def test_read_note_incorrect_id(test_app, monkeypatch):
    async def mock_get(self, note_id):
        return None

    monkeypatch.setattr("app.database.MongoManager.get_note", mock_get)

    response = test_app.get("/notes/1")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "ObjectId invalid"


def test_read_all_notes(test_app, monkeypatch, test_note_db, test_note_db_1):
    test_data = [
        test_note_db,
        test_note_db_1,
    ]

    async def mock_get_all(self):
        return test_data

    monkeypatch.setattr("app.database.MongoManager.get_notes", mock_get_all)

    response = test_app.get("/notes/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_update_note(test_app, monkeypatch, test_note, test_note_db, test_oid):
    async def mock_put(self, note_id, note):
        return test_note

    monkeypatch.setattr("app.database.MongoManager.update_note", mock_put)

    response = test_app.put(f"/notes/{test_oid}", data=json.dumps(test_note))
    assert response.status_code == 200
    assert response.json() == test_note_db


def test_remove_note(test_app, monkeypatch, test_oid):
    async def mock_delete(self, note_id):
        return None

    monkeypatch.setattr("app.database.MongoManager.delete_note", mock_delete)

    response = test_app.delete(f"/notes/{test_oid}")
    assert response.status_code == 204


def test_remove_note_incorrect_id(test_app, monkeypatch):
    response = test_app.delete("/notes/1")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "ObjectId invalid"
