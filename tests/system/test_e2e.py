# System-level test (end-to-end) -- spins up the FastAPI app with TestClient
from fastapi.testclient import TestClient
from app.main import app

def test_e2e_full_flow():
    client = TestClient(app)
    
    ids = []
    for i in range(3):
        r = client.post('/users/', json={'name': f'System user {i}', 'email': f'u{i}@ex.com'})
        assert r.status_code == 201
        ids.append(r.json()['id'])

    
    r = client.get('/users/')
    assert r.status_code == 200
    users = r.json()
    assert len(users) >= 3

    
    for uid in ids:
        r = client.delete(f'/users/{uid}')
        assert r.status_code == 204
