import pytest
from sqlmodel import SQLModel
from sqlmodel import Session, create_engine
from app.models import UserCreate, UserUpdate, User, TaskCreate, TaskUpdate, Task
from app import crud


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        yield s


def test_create_and_get_user(session):
    payload = UserCreate(name='Alice', email='alice@example.com')
    user = crud.create_user(session, payload)
    assert user.id is not None
    fetched = crud.get_user(session, user.id)
    assert fetched.name == 'Alice'


def test_update_and_delete_user(session):
    payload = UserCreate(name='Bob', email='bob@example.com')
    user = crud.create_user(session, payload)
    upd = UserUpdate(name='Bobby')
    updated = crud.update_user(session, user.id, upd)
    assert updated.name == 'Bobby'
    ok = crud.delete_user(session, user.id)
    assert ok is True
    assert crud.get_user(session, user.id) is None


def test_create_task_for_user_and_crud(session):
    user_payload = UserCreate(name='Carl', email='carl@example.com')
    user = crud.create_user(session, user_payload)

    task_payload = TaskCreate(title='Task 1', description='desc', user_id=user.id)
    task = crud.create_task(session, task_payload)
    assert task.id is not None
    assert task.user_id == user.id

    fetched = crud.get_task(session, task.id)
    assert fetched.title == 'Task 1'

    upd = TaskUpdate(title='Task 1 updated', is_completed=True)
    updated = crud.update_task(session, task.id, upd)
    assert updated.title == 'Task 1 updated'
    assert updated.is_completed is True

    ok = crud.delete_task(session, task.id)
    assert ok is True
    assert crud.get_task(session, task.id) is None
