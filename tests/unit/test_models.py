from app.models import UserCreate, UserUpdate, TaskCreate, TaskUpdate


def test_user_create_model():
    # Probar que se crea correctamente
    user = UserCreate(name="Ana", email="ana@test.com")
    assert user.name == "Ana"
    assert user.email == "ana@test.com"


def test_user_update_model():
    # Probar campos opcionales
    update = UserUpdate(name="Ana Updated")
    assert update.name == "Ana Updated"
    assert update.email is None  # No se envió


def test_task_create_model():
    # user_id obligatorio
    task = TaskCreate(title="Hacer parcial", user_id=1)
    assert task.title == "Hacer parcial"
    assert task.user_id == 1
    assert task.is_completed is False


def test_task_update_model():
    # Solo algunos campos
    update = TaskUpdate(is_completed=True)
    assert update.is_completed is True
    assert update.title is None