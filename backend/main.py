# Ponto de entrada principal da aplicação FastAPI

# Imports de bibliotecas externas
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy import create_engine
import os

# --- Bloco de Importações Locais Corrigido ---
from . import crud
from . import models
from . import security
from .database import database, connect_db, disconnect_db, metadata
from .schemas import User, Token, UserCreate, Task, TaskCreate
from sqlalchemy import create_engine
import os

# --- Configuração Inicial ---

# Define o diretório base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL_SYNC = f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}" # URL síncrona para criação de tabelas

# Cria as tabelas no banco de dados se não existirem (usando engine síncrono)
def create_db_and_tables():
    engine = create_engine(DATABASE_URL_SYNC, connect_args={"check_same_thread": False})
    metadata.create_all(bind=engine)

# Cria as tabelas ao iniciar
create_db_and_tables()

app = FastAPI(title="API Lista de Tarefas Colaborativa")

# Configuração do CORS (ajustar origens em produção)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permitir todas as origens por enquanto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Eventos de inicialização e finalização da aplicação
@app.on_event("startup")
async def startup():
    await connect_db()

@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()

# --- Autenticação --- 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = security.decode_access_token(token)
    if email is None:
        raise credentials_exception
    user = await crud.get_user_by_email(email=email)
    if user is None:
        raise credentials_exception
    # Retorna o objeto do usuário (pode ser um dict ou um objeto Pydantic/SQLAlchemy)
    # Convertendo o resultado do banco (Row) para um schema Pydantic para tipagem
    return User.model_validate(user)

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# --- Rotas --- 

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud.get_user_by_email(email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    db_user = await crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    created_user = await crud.create_user(user=user)
    # Convertendo o dict retornado pelo CRUD para o schema Pydantic
    return User.model_validate(created_user)

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.post("/tasks/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task_for_user(
    task: TaskCreate,
    current_user: User = Depends(get_current_active_user)
):
    created_task = await crud.create_task(task=task, owner_id=current_user.id)
    # Convertendo o resultado do banco (Row) para o schema Pydantic
    return Task.model_validate(created_task)

@app.get("/tasks/", response_model=List[Task])
async def read_tasks(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    tasks = await crud.get_tasks_by_owner(owner_id=current_user.id, skip=skip, limit=limit)
    # Convertendo a lista de Rows para uma lista de schemas Pydantic
    return [Task.model_validate(task) for task in tasks]

@app.patch("/tasks/{task_id}/complete", status_code=status.HTTP_204_NO_CONTENT)
async def mark_task_complete(task_id: int, current_user: User = Depends(get_current_active_user)):
    result = await crud.update_task_status(task_id=task_id, completed=True, owner_id=current_user.id)
    if result == 0:
        raise HTTPException(status_code=404, detail="Task not found or not owned by user")
    return

@app.patch("/tasks/{task_id}/incomplete", status_code=status.HTTP_204_NO_CONTENT)
async def mark_task_incomplete(task_id: int, current_user: User = Depends(get_current_active_user)):
    result = await crud.update_task_status(task_id=task_id, completed=False, owner_id=current_user.id)
    if result == 0:
        raise HTTPException(status_code=404, detail="Task not found or not owned by user")
    return

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, current_user: User = Depends(get_current_active_user)):
    result = await crud.delete_task(task_id=task_id, owner_id=current_user.id)
    if result == 0:
        raise HTTPException(status_code=404, detail="Task not found or not owned by user")
    return

@app.get("/")
async def root():
    return {"message": "API da Lista de Tarefas está funcionando!"}