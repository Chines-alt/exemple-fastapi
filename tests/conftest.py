import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import oauth2



from app.main import app
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models
from app.config import settings
from uuid import uuid4



SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:{settings.database_password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)



@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    unique_email = f"{uuid4()}@example.com"
    user_data = {
        "email": unique_email,
        "password": "testpassword"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    user = response.json()
    user["password"] = user_data["password"]
    return user

@pytest.fixture
def token(test_user):
    return oauth2.create_access_token(data={"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, test_user):  # добавили зависимость от test_user
    token = oauth2.create_access_token(data={"user_id": test_user["id"]})
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, session):
    posts_data = [
        {
            "title": "First Post",
            "content": "Content of the first post",
            "owner_id": test_user["id"]
        },
        {
            "title": "Second Post",
            "content": "Content of the second post",
            "owner_id": test_user["id"]
        }
    ]
    

    def create_post_model(post):
        return models.Post(**post)

    posts = list(map(create_post_model, posts_data))
    session.add_all(posts)
    session.commit()
    return session.query(models.Post).all()