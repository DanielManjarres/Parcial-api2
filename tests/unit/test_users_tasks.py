import pytest
from sqlmodel import SQLModel, Session, create_engine
from app.models import UserCreate, UserUpdate, TaskCreate, TaskUpdate
from app import crud


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        yield s


def test_user_full_crud_cycle(session):
    # Crear usuario
    user = crud.create_user(session, UserCreate(name="Ana", email="ana@test.com"))
    assert user.id is not None

    # Leer
    fetched = crud.get_user(session, user.id)
    assert fetched.name == "Ana"

    # Actualizar
    updated = crud.update_user(session, user.id, UserUpdate(name="Ana Updated"))
    assert updated.name == "Ana Updated"

    # Eliminar
    assert crud.delete_user(session, user.id) is True
    assert crud.get_user(session, user.id) is None


def test_task_full_crud_cycle_with_user(session):
    # Crear usuario primero
    user = crud.create_user(session, UserCreate(name="Luis", email="luis@test.com"))

    # Crear tarea asociada
    task = crud.create_task(session, TaskCreate(title="Estudiar", user_id=user.id))
    assert task.user_id == user.id

    # Leer
    fetched = crud.get_task(session, task.id)
    assert fetched.title == "Estudiar"

    # Actualizar (completar)
    updated = crud.update_task(session, task.id, TaskUpdate(is_completed=True))
    assert updated.is_completed is True

    # Eliminar
    assert crud.delete_task(session, task.id) is True
    assert crud.get_task(session, task.id) is None