from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
from app.main import app
from app.database import engine as real_engine
from app import database
import os
import tempfile

def get_temp_db_url(tmp_path):
    return f"sqlite:///{tmp_path / 'db.sqlite'}"

def test_create_list_get_patch_delete(tmp_path, monkeypatch):
    db_url = get_temp_db_url(tmp_path)
    monkeypatch.setenv('DATABASE_URL', db_url)
    from importlib import reload
    reload(database)
    database.init_db()

    client = TestClient(app)

    resp = client.post('/users/', json={'name': 'Integration User', 'email': 'i@example.com'})
    assert resp.status_code == 201
    user = resp.json()

    resp = client.post('/tasks/', json={'title':'Integracion task', 'user_id': user['id']})
    assert resp.status_code == 201
    data = resp.json()
    assert data['title'] == 'Integracion task'
    task_id = data['id']

    resp = client.get('/tasks/')
    assert resp.status_code == 200
    assert any(t['id'] == task_id for t in resp.json())

    resp = client.get(f'/tasks/{task_id}')
    assert resp.status_code == 200

    resp = client.patch(f'/tasks/{task_id}', json={'is_completed': True})
    assert resp.status_code == 200
    assert resp.json()['is_completed'] is True

    resp = client.delete(f'/tasks/{task_id}')
    assert resp.status_code == 204

    resp = client.get(f'/tasks/{task_id}')
    assert resp.status_code == 404
