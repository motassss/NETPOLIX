import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine_test = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def override_get_db():
    Base.metadata.create_all(bind=engine_test)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


def test_registro_exitoso():
    response = client.post("/auth/registro", json={
        "nombre": "Test User",
        "cedula": "1234567890",
        "password": "testpassword",
    })
    assert response.status_code == 201
    data = response.json()
    assert "cedula" in data
    assert data["cedula"] == "1234567890"


def test_registro_cedula_duplicada():
    client.post("/auth/registro", json={
        "nombre": "User 1",
        "cedula": "1111111111",
        "password": "testpassword",
    })
    response = client.post("/auth/registro", json={
        "nombre": "User 2",
        "cedula": "1111111111",
        "password": "testpassword",
    })
    assert response.status_code == 400
    assert "ya existe" in response.json()["detail"].lower()


def test_login_exitoso():
    client.post("/auth/registro", json={
        "nombre": "Test User",
        "cedula": "0987654321",
        "password": "testpassword",
    })
    response = client.post("/auth/login", json={
        "cedula": "0987654321",
        "password": "testpassword",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_contraseña_incorrecta():
    client.post("/auth/registro", json={
        "nombre": "Test User",
        "cedula": "1122334455",
        "password": "testpassword",
    })
    response = client.post("/auth/login", json={
        "cedula": "1122334455",
        "password": "wrongpassword",
    })
    assert response.status_code == 401


def test_acceso_protegido_sin_token():
    response = client.get("/videos/")
    assert response.status_code == 401


def test_acceso_protegido_con_token():
    client.post("/auth/registro", json={
        "nombre": "Test User",
        "cedula": "5555555555",
        "password": "testpassword",
    })
    login_resp = client.post("/auth/login", json={
        "cedula": "5555555555",
        "password": "testpassword",
    })
    token = login_resp.json()["access_token"]
    response = client.get(
        "/videos/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
