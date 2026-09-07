from typing import Generator
from sqlmodel import create_engine, Session, SQLModel
from core.config import settings

# engine única e centralizada para a aplicação
engine = create_engine(settings.DATABASE_URL, echo=True)

def init_db() -> None:
    """Cria as tabelas no banco de dados se não existirem."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Injeção de dependência do FastAPI para gerenciar a sessão do banco."""
    with Session(engine) as session:
        yield session