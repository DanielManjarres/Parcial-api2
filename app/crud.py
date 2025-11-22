from sqlmodel import Session, select
from .models import (
    User,
    UserCreate,
    UserUpdate,
    Task,
    TaskCreate,
    TaskUpdate,
)


def create_user(session: Session, payload: UserCreate) -> User:
    user = User.from_orm(payload)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)


def list_users(session: Session):
    return session.exec(select(User)).all()


def update_user(session: Session, user_id: int, payload: UserUpdate):
    user = session.get(User, user_id)
    if not user:
        return None
    user_data = payload.dict(exclude_unset=True)
    for k, v in user_data.items():
        setattr(user, k, v)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user_id: int) -> bool:
    user = session.get(User, user_id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True


def create_task(session: Session, payload: TaskCreate) -> Task:
    task = Task.from_orm(payload)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_task(session: Session, task_id: int) -> Task | None:
    return session.get(Task, task_id)


def list_tasks(session: Session):
    return session.exec(select(Task)).all()


def update_task(session: Session, task_id: int, payload: TaskUpdate):
    task = session.get(Task, task_id)
    if not task:
        return None
    task_data = payload.dict(exclude_unset=True)
    for k, v in task_data.items():
        setattr(task, k, v)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task_id: int) -> bool:
    task = session.get(Task, task_id)
    if not task:
        return False
    session.delete(task)
    session.commit()
    return True
