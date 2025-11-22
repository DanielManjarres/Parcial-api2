from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


# ==================== TABLAS ====================
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    tasks: List["Task"] = Relationship(back_populates="user")


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="tasks")


# ==================== DTOs (para entrada/salida) ====================
class UserCreate(SQLModel):
    name: str
    email: str


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None


class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    user_id: int  # Obligatorio para que no haya tareas huérfanas


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    