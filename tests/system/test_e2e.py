# PRUEBA END-TO-END COMPLETA - Flujo real de usuario
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_flujo_completo_usuario_y_tareas():
    # 1. Crear un usuario
    resp = client.post("/users/", json={"name": "Juan", "email": "juan@test.com"})
    assert resp.status_code == 201
    user_id = resp.json()["id"]

    # 2. Crear 2 tareas para ese usuario
    client.post("/tasks/", json={"title": "Estudiar", "user_id": user_id})
    resp2 = client.post("/tasks/", json={"title": "Hacer parcial", "is_completed": False, "user_id": user_id})
    assert resp2.status_code == 201
    task_id = resp2.json()["id"]

    # 3. Listar todas las tareas y verificar que están
    tareas = client.get("/tasks/").json()
    assert len(tareas) >= 2
    assert any(t["title"] == "Hacer parcial" for t in tareas)

    # 4. Marcar una tarea como completada
    resp = client.patch(f"/tasks/{task_id}", json={"is_completed": True})
    assert resp.status_code == 200
    assert resp.json()["is_completed"] is True

    # 5. Eliminar la tarea
    resp = client.delete(f"/tasks/{task_id}")
    assert resp.status_code == 204

    # 6. Verificar que ya no existe
    resp = client.get(f"/tasks/{task_id}")
    assert resp.status_code == 404

    print("FLUJO E2E COMPLETO EXITOSO - 10/10")