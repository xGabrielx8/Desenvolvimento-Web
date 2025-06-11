# Configuração do banco de dados SQLite
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

# Define o diretório base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite+aiosqlite:///{os.path.join(BASE_DIR, 'app.db')}" # Usando aiosqlite para async

# Configuração para SQLAlchemy ORM síncrono (se necessário para algumas operações ou libs)
# engine_sync = create_engine(DATABASE_URL.replace("+aiosqlite", ""), connect_args={"check_same_thread": False})
# SessionLocalSync = sessionmaker(autocommit=False, autoflush=False, bind=engine_sync)

# Configuração para SQLAlchemy Core e `databases` assíncrono
database = Database(DATABASE_URL)
metadata = MetaData()

# Base para modelos ORM (se usar ORM assíncrono ou síncrono)
Base = declarative_base(metadata=metadata)

# Função para criar tabelas (executar uma vez na inicialização, se necessário)
async def create_tables():
    # engine = create_engine(DATABASE_URL.replace("+aiosqlite", ""), connect_args={"check_same_thread": False})
    # Base.metadata.create_all(bind=engine)
    # Para `databases`, as tabelas são geralmente definidas no `models.py` e criadas manualmente ou com migrations
    pass

# Funções para conectar e desconectar o banco de dados assíncrono
async def connect_db():
    await database.connect()

async def disconnect_db():
    await database.disconnect()

