import pytest
from sqlmodel import SQLModel, Session, create_engine
from app.models import UserCreate, UserUpdate, TaskCreate, TaskUpdate
from app import crud


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    # Se cierra automáticamente al salir del bloque


def test_user_crud_full_cycle(session: Session):
    # CREATE
    payload = UserCreate(name="Alice", email="alice@example.com")
    user = crud.create_user(session, payload)
    assert user.id is not None
    assert user.name == "Alice"
    assert user.email == "alice@example.com"

    # READ
    fetched = crud.get_user(session, user.id)
    assert fetched == user

    # UPDATE
    update_payload = UserUpdate(name="Alice Updated", email="new@mail.com")
    updated = crud.update_user(session, user.id, update_payload)
    assert updated.name == "Alice Updated"
    assert updated.email == "new@mail.com"

    # LIST
    all_users = crud.list_users(session)
    assert len(all_users) == 1
    assert all_users[0].id == user.id

    # DELETE
    deleted = crud.delete_user(session, user.id)
    assert deleted is True
    assert crud.get_user(session, user.id) is None


def test_task_crud_full_cycle(session: Session):
    # Primero creamos un usuario
    user = crud.create_user(session, UserCreate(name="Bob", email="bob@test.com"))
    user_id = user.id

    # CREATE Task
    task_data = TaskCreate(title="Hacer el parcial", user_id=user_id)
    task = crud.create_task(session, task_data)
    assert task.id is not None
    assert task.title == "Hacer el parcial"
    assert task.user_id == user_id
    assert task.is_completed is False

    # READ
    fetched = crud.get_task(session, task.id)
    assert fetched == task

    # UPDATE
    update_data = TaskUpdate(is_completed=True, title="Parcial hecho!")
    updated_task = crud.update_task(session, task.id, update_data)
    assert updated_task.is_completed is True
    assert updated_task.title == "Parcial hecho!"

    # LIST
    tasks = crud.list_tasks(session)
    assert len(tasks) == 1
    assert tasks[0].is_completed is True

    # DELETE
    deleted = crud.delete_task(session, task.id)
    assert deleted is True
    assert crud.get_task(session, task.id) is None