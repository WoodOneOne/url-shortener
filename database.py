from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

database_file = Path(__file__).resolve().with_name("links.db")
database_url = f"sqlite:///{database_file.as_posix()}"

engine = create_engine(
    database_url, connect_args={"check_same_thread": False}
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session