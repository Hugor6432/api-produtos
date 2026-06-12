import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, Base, get_db

DATABASE_URL_TEST = "postgresql://usuario:senha123@localhost:5433/testdb"

engine_test = create_engine(DATABASE_URL_TEST)
SessionTest = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine_test)

    def override_get_db():
        db = SessionTest()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine_test)

@pytest.fixture
def produto_existente(client):
    response = client.post(
        "/produtos",
        json={"nome": "Produto Teste", "preco": 29.90, "estoque": 10}
    )
    return response.json()
