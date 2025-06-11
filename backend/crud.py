# Funções CRUD para interagir com o banco de dados
import datetime
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession # Se estivesse usando ORM assíncrono

from . import models
from . import schemas
from . import security
from .database import database

# --- CRUD Usuários ---

async def get_user_by_email(email: str):
    """Busca um usuário pelo email."""
    query = select(models.users).where(models.users.c.email == email)
    return await database.fetch_one(query)

async def get_user(user_id: int):
    """Busca um usuário pelo ID."""
    query = select(models.users).where(models.users.c.id == user_id)
    return await database.fetch_one(query)

async def create_user(user: schemas.UserCreate):
    """Cria um novo usuário no banco de dados."""
    hashed_password = security.get_password_hash(user.password)
    query = insert(models.users).values(
        email=user.email,
        hashed_password=hashed_password,
        is_active=True # Ativar por padrão
    )
    last_record_id = await database.execute(query)
    return {**user.model_dump(exclude={"password"}), "id": last_record_id, "is_active": True}

# --- CRUD Tarefas ---

async def get_tasks_by_owner(owner_id: int, skip: int = 0, limit: int = 100):
    """Lista as tarefas de um usuário específico."""
    query = select(models.tasks).where(models.tasks.c.owner_id == owner_id).offset(skip).limit(limit)
    return await database.fetch_all(query)

async def create_task(task: schemas.TaskCreate, owner_id: int):
    """Cria uma nova tarefa para um usuário."""
    
    # Adicionamos a data de criação manualmente aqui
    query = insert(models.tasks).values(
        title=task.title,
        description=task.description,
        completed=False, 
        owner_id=owner_id,
        created_at=datetime.datetime.now() # Garante que a data nunca será nula
    )
    
    last_record_id = await database.execute(query)
    
    # Busca a tarefa recém-criada para retornar o objeto completo
    created_task_query = select(models.tasks).where(models.tasks.c.id == last_record_id)
    return await database.fetch_one(created_task_query)

async def update_task_status(task_id: int, completed: bool, owner_id: int):
    """Atualiza o status (concluída/não concluída) de uma tarefa."""
    query = update(models.tasks).where(
        models.tasks.c.id == task_id,
        models.tasks.c.owner_id == owner_id # Garante que só o dono pode atualizar
    ).values(completed=completed)
    result = await database.execute(query)
    return result # Retorna o número de linhas afetadas (1 se sucesso, 0 se não encontrou/não pertence ao user)

async def delete_task(task_id: int, owner_id: int):
    """Deleta uma tarefa."""
    query = delete(models.tasks).where(
        models.tasks.c.id == task_id,
        models.tasks.c.owner_id == owner_id # Garante que só o dono pode deletar
    )
    result = await database.execute(query)
    return result # Retorna o número de linhas afetadas (1 se sucesso, 0 se não encontrou/não pertence ao user)
async def update_task_status(task_id: int, completed: bool, owner_id: int):
    """Atualiza o status (concluída/não concluída) de uma tarefa."""
    query = update(models.tasks).where(
        models.tasks.c.id == task_id,
        models.tasks.c.owner_id == owner_id
    ).values(completed=completed)
    result = await database.execute(query)
    return result

async def delete_task(task_id: int, owner_id: int):
    query = delete(models.tasks).where(
        models.tasks.c.id == task_id,
        models.tasks.c.owner_id == owner_id
    )
    result = await database.execute(query)
    return result
