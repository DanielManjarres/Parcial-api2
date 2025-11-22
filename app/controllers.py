from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from .database import get_session
from .models import User, UserCreate, UserUpdate, Task, TaskCreate, TaskUpdate
from . import services

router = APIRouter()


@router.post("/users/", response_model=User, status_code=201)
def create_user_endpoint(payload: UserCreate, session: Session = Depends(get_session)):
    return services.create_user(session, payload)


@router.get("/users/{user_id}", response_model=User)
def get_user_endpoint(user_id: int, session: Session = Depends(get_session)):
    user = services.get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/", response_model=list[User])
def list_users_endpoint(session: Session = Depends(get_session)):
    return services.list_users(session)


@router.patch("/users/{user_id}", response_model=User)
def update_user_endpoint(user_id: int, payload: UserUpdate, session: Session = Depends(get_session)):
    user = services.update_user(session, user_id, payload)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}", status_code=204)
def delete_user_endpoint(user_id: int, session: Session = Depends(get_session)):
    ok = services.delete_user(session, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")



@router.post("/tasks/", response_model=Task, status_code=201)
def create_task_endpoint(payload: TaskCreate, session: Session = Depends(get_session)):
    return services.create_task(session, payload)


@router.get("/tasks/{task_id}", response_model=Task)
def get_task_endpoint(task_id: int, session: Session = Depends(get_session)):
    task = services.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/tasks/", response_model=list[Task])
def list_tasks_endpoint(session: Session = Depends(get_session)):
    return services.list_tasks(session)


@router.patch("/tasks/{task_id}", response_model=Task)
def update_task_endpoint(task_id: int, payload: TaskUpdate, session: Session = Depends(get_session)):
    task = services.update_task(session, task_id, payload)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task_endpoint(task_id: int, session: Session = Depends(get_session)):
    ok = services.delete_task(session, task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found")


