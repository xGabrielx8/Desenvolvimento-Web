# Definição dos schemas Pydantic (modelos de dados da API)
from pydantic import BaseModel
from typing import Optional, List
import datetime

# --- Schemas de Tarefas ---

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    completed: bool # <-- CAMPO ADICIONADO DE VOLTA
    created_at: datetime.datetime
    owner_id: int

    class Config:
        from_attributes = True

# --- Schemas de Usuários (sem alterações) ---

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    tasks: List[Task] = []

    class Config:
        from_attributes = True

# --- Schemas de Token (sem alterações) ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
