from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from alembic import command

from app import models
from app.database import get_db, Base
from app.main import app
from app.config import settings
from app.oauth2 import create_access_token


# SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://postgres:postgres@localhost:5432/fastapi_test"
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

    # command.upgrade("head")
    # yield TestClient(app)
    # command.downgrade("base")


def create_test_user(client, email, password):
    user_data = {
        "email": email,
        "password": password,
    }
    res = client.post(
        "/users/",
        json=user_data
    )
    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user(client):
    return create_test_user(
        client, 
        email="dayyass@yandex.ru",
        password="password123",
    )


@pytest.fixture
def test_user2(client):
    return create_test_user(
        client, 
        email="dayyass2@yandex.ru",
        password="password123",
    )


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def autorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(session, test_user, test_user2):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user['id']
        },
        {
            "title": "2nd title",
            "content": "2nd content",
            "owner_id": test_user['id']
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": test_user['id']
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": test_user2['id']
        },
    ]

    session.add_all([models.Post(**post_data) for post_data in posts_data])
    session.commit()

    posts = session.query(models.Post).all()
    return posts
