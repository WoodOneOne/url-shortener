import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from database import get_session
from main import app


@pytest.fixture
def client(tmp_path):
    database_file = tmp_path / "test.db"
    database_url = f"sqlite:///{database_file.as_posix()}"

    test_engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
    )

    SQLModel.metadata.create_all(test_engine)

    def override_get_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    test_client = TestClient(app)
    yield test_client

    test_client.close()
    app.dependency_overrides.clear()
