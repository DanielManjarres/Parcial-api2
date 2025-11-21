import pytest
from sqlmodel import SQLModel
from sqlmodel import Session, create_engine
from app.models import (
    UserCreate,
    UserUpdate,
    TaskCreate,
    TaskUpdate,
)
from app import crud


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        yield s


def test_user_crud(session):
   
    payload = UserCreate(name='Alice', email='alice@example.com')
    user = crud.create_user(session, payload)
    assert user.id is not None

  
    fetched = crud.get_user(session, user.id)
    assert fetched is not None
    assert fetched.name == 'Alice'

    upd = UserUpdate(name='Alice Updated')
    updated = crud.update_user(session, user.id, upd)
    assert updated is not None
    assert updated.name == 'Alice Updated'

    users = crud.list_users(session)
    assert any(u.id == user.id for u in users)

    ok = crud.delete_user(session, user.id)
    assert ok is True
    assert crud.get_user(session, user.id) is None


def test_task_crud(session):
    user = crud.create_user(session, UserCreate(name='Bob', email='bob@example.com'))

    task_payload = TaskCreate(title='Task 1', description='desc', user_id=user.id)
    task = crud.create_task(session, task_payload)
    assert task.id is not None
    assert task.user_id == user.id

    fetched = crud.get_task(session, task.id)
    assert fetched is not None
    assert fetched.title == 'Task 1'

    upd = TaskUpdate(title='Task 1 updated', is_completed=True)
    updated = crud.update_task(session, task.id, upd)
    assert updated is not None
    assert updated.title == 'Task 1 updated'
    assert updated.is_completed is True

    tasks = crud.list_tasks(session)
    assert any(t.id == task.id for t in tasks)

    ok = crud.delete_task(session, task.id)
    assert ok is True
    assert crud.get_task(session, task.id) is None
