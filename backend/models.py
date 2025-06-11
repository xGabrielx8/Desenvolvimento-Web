# Definição das tabelas do banco de dados (SQLAlchemy Core)
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, MetaData, DateTime
from .database import metadata
import datetime

# Tabela de Usuários
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("email", String, unique=True, index=True, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True),
    # Adicionar coluna para papel (Admin/Usuário Comum) se necessário, conforme template
    # Column("role", String, default="Usuário Comum")
)

# Tabela de Tarefas
tasks = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("title", String, index=True, nullable=False),
    Column("description", String, nullable=True),
    Column("completed", Boolean, default=False),
    Column("created_at", DateTime, default=datetime.datetime.utcnow),
    Column("owner_id", Integer, ForeignKey("users.id"), nullable=False),
)

# Nota: A criação real das tabelas no banco de dados SQLite
# será feita na inicialização da aplicação ou através de um script de migração.
# A função `create_tables` em `database.py` pode ser adaptada para isso
# usando `metadata.create_all(engine)` se um engine síncrono for usado
# ou executando comandos SQL diretamente com a conexão assíncrona.

