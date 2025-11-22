from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from .database import get_session
from .models import (
    User, UserCreate, UserUpdate,
    Task, TaskCreate, TaskUpdate
)
from . import services

router = APIRouter(tags=["users", "tasks"]) 


# ====================== USERS ======================
@router.post(
    "/users/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
    response_description="Usuario creado exitosamente"
)
def create_user(payload: UserCreate, session: Session = Depends(get_session)):
    return services.create_user(session, payload)


@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = services.get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/", response_model=List[User])
def list_users(session: Session = Depends(get_session)):
    return services.list_users(session)


@router.patch("/users/{user_id}", response_model=User)
def update_user(user_id: int, payload: UserUpdate, session: Session = Depends(get_session)):
    user = services.update_user(session, user_id, payload)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    if not services.delete_user(session, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return None


# ====================== TASKS ======================
@router.post(
    "/tasks/",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva tarea",
    description="La tarea debe pertenecer a un usuario existente (user_id obligatorio)"
)
def create_task(payload: TaskCreate, session: Session = Depends(get_session)):
    return services.create_task(session, payload)


@router.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int, session: Session = Depends(get_session)):
    task = services.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/tasks/", response_model=List[Task])
def list_tasks(session: Session = Depends(get_session)):
    return services.list_tasks(session)


@router.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskUpdate, session: Session = Depends(get_session)):
    task = services.update_task(session, task_id, payload)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    if not services.delete_task(session, task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return None
