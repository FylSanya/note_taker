import json


def test_add_template(test_app, monkeypatch, test_template):
    async def mock_template(self, payload):
        return None

    monkeypatch.setattr("app.database.MongoManager.add_template", mock_template)
    response = test_app.post("/templates/", data=json.dumps(test_template))

    assert response.status_code == 201
    assert response.json() is None


def test_add_template_invalid_json(test_app):
    response = test_app.post("/templates/", data=json.dumps({"title": "something"}))
    assert response.status_code == 422


def test_get_template(test_app, monkeypatch, test_template_db, test_template_oid):
    async def mock_get(self, template_id):
        return test_template_db

    monkeypatch.setattr("app.database.MongoManager.get_template", mock_get)

    response = test_app.get(f"/templates/{test_template_oid}")
    assert response.status_code == 200
    assert response.json() == test_template_db


def test_read_template_incorrect_id(test_app, monkeypatch):
    async def mock_get(self, template_id):
        return None

    monkeypatch.setattr("app.database.MongoManager.get_template", mock_get)

    response = test_app.get("/templates/1")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "ObjectId invalid"


def test_read_all_templates(test_app, monkeypatch, test_template_db, test_template_db_1):
    test_data = [
        test_template_db,
        test_template_db_1,
    ]

    async def mock_get_all(self):
        return test_data

    monkeypatch.setattr("app.database.MongoManager.get_templates", mock_get_all)

    response = test_app.get("/templates/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_update_template(test_app, monkeypatch, test_template, test_template_db, test_template_oid):
    async def mock_put(self, template_id, template):
        return test_template

    monkeypatch.setattr("app.database.MongoManager.update_template", mock_put)

    response = test_app.put(f"/templates/{test_template_oid}", data=json.dumps(test_template))
    assert response.status_code == 200
    assert response.json() == test_template_db


def test_remove_template(test_app, monkeypatch, test_template_oid):
    async def mock_delete(self, template_id):
        return None

    monkeypatch.setattr("app.database.MongoManager.delete_template", mock_delete)

    response = test_app.delete(f"/templates/{test_template_oid}")
    assert response.status_code == 204


def test_remove_template_incorrect_id(test_app, monkeypatch):
    response = test_app.delete("/templates/1")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "ObjectId invalid"
