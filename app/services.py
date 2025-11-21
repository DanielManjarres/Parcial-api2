from sqlmodel import Session
from . import crud
from .models import User, UserCreate, UserUpdate, Task, TaskCreate, TaskUpdate


def create_user(session: Session, payload: UserCreate) -> User:
    return crud.create_user(session, payload)


def get_user(session: Session, user_id: int) -> User | None:
    return crud.get_user(session, user_id)


def list_users(session: Session):
    return crud.list_users(session)


def update_user(session: Session, user_id: int, payload: UserUpdate):
    return crud.update_user(session, user_id, payload)


def delete_user(session: Session, user_id: int) -> bool:
    return crud.delete_user(session, user_id)


# Task services
def create_task(session: Session, payload: TaskCreate) -> Task:
    return crud.create_task(session, payload)


def get_task(session: Session, task_id: int) -> Task | None:
    return crud.get_task(session, task_id)


def list_tasks(session: Session):
    return crud.list_tasks(session)


def update_task(session: Session, task_id: int, payload: TaskUpdate):
    return crud.update_task(session, task_id, payload)


def delete_task(session: Session, task_id: int) -> bool:
    return crud.delete_task(session, task_id)
