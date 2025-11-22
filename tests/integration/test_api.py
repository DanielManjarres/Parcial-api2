from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db
from sqlmodel import SQLModel, create_engine, Session

# Usamos base de datos en memoria solo para este test
test_engine = create_engine("sqlite:///:memory:")
SQLModel.metadata.create_all(test_engine)

# Sobreescribimos la dependencia real por una de prueba
def override_get_session():
    with Session(test_engine) as session:
        yield session

app.dependency_overrides[app.dependency_overrides.get("get_session", lambda: None)] = override_get_session

client = TestClient(app)

def test_full_flow():
    # 1. Crear usuario
    resp = client.post("/users/", json={"name": "Test User", "email": "test@example.com"})
    assert resp.status_code == 201
    user = resp.json()
    user_id = user["id"]

    # 2. Crear tarea
    resp = client.post("/tasks/", json={"title": "Mi tarea", "user_id": user_id})
    assert resp.status_code == 201
    task = resp.json()
    task_id = task["id"]

    # 3. Listar tareas
    resp = client.get("/tasks/")
    assert resp.status_code == 200
    tasks = resp.json()
    assert any(t["id"] == task_id for t in tasks)

    # 4. Actualizar tarea (marcar como completada)
    resp = client.patch(f"/tasks/{task_id}", json={"is_completed": True})
    assert resp.status_code == 200
    assert resp.json()["is_completed"] is True

    # 5. Eliminar tarea
    resp = client.delete(f"/tasks/{task_id}")
    assert resp.status_code == 204

    # 6. Verificar que ya no existe
    resp = client.get(f"/tasks/{task_id}")
    assert resp.status_code == 404

    print("TEST DE INTEGRACIÓN COMPLETO - 10/10")