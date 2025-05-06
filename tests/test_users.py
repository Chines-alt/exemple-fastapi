import pytest
from jose import jwt
from app import schemas
from app.config import settings



@pytest.fixture(autouse=True)
def test_user(client):
    user_data = {"email": "hello323@gmail.com", "password": "hello123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    user = response.json()
    user["password"] = user_data["password"]
    return user


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json().get("message") == "Hello World!!!!!!!!"


def test_create_user(client):
    response = client.post("/users/", json={"email": "hello321113@gmail.com", "password": "hello123"})
    assert response.status_code == 201
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "hello321113@gmail.com"


def test_login_user(client, test_user):
    response = client.post("/login", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    assert response.status_code == 200

    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    user_id = payload.get("user_id")

    assert user_id == test_user["id"]
    assert login_response.token_type == "bearer"


@pytest.fixture
def token(test_user):
    from app import oauth2  # важно: должен быть импорт oauth2
    return oauth2.create_access_token(data={"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client
