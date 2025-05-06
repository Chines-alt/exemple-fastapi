import pytest
from app import schemas
from app import models



def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, response.json())
    posts_list = list(posts_map)
   
    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401

def test_unauthorized_user_get_one_posts(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/88888")
    assert response.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 200
    post = schemas.PostOut(**response.json())  # валидируем через схему
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize("title, content, published", [
    ("Updated Title 1", "Updated Content 1", True),
    ("Updated Title 2", "Updated Content 2", False),
    ("Updated Title 3", "Updated Content 3", True),
])
def test_create_post(authorized_client, title, content, published):
    response = authorized_client.post("/posts/", json={
        "title": title,
        "content": content,
        "published": published
    })
    assert response.status_code == 201
    assert response.json()["title"] == title
    assert response.json()["content"] == content
    assert response.json()["published"] == published

def test_create_post_default_published_true(authorized_client):
    post_data = {
        "title": "Default Published Post",
        "content": "Content without specifying 'published'"
    }
    response = authorized_client.post("/posts/", json=post_data)
    created_post = response.json()
    
    assert response.status_code == 201
    assert created_post["title"] == post_data["title"]
    assert created_post["content"] == post_data["content"]
    assert created_post["published"] == True

def test_unauthorized_create_posts(client):
    post_data = {
        "title": "Should Fail",
        "content": "This should not be allowed",
        "published": True
    }
    response = client.post("/posts/", json=post_data)
    assert response.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    print(f"Authorized User ID: {test_user['id']}")
    print(f"Post Owner ID: {test_posts[0].owner_id}")
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204

def test_delete_post_non_exist(authorized_client):
    
    response = authorized_client.delete("/posts/999999")
    assert response.status_code == 404


def test_delete_other_user_post(authorized_client, test_other_user_post):
    response = authorized_client.delete(f"/posts/{test_other_user_post.id}")
    assert response.status_code == 403
 

@pytest.fixture
def test_other_user_post(session):
    other_user = models.User(email="other@example.com", password="testpass")
    session.add(other_user)
    session.commit()

    post = models.Post(title="Other's post", content="Not yours", owner_id=other_user.id)
    session.add(post)
    session.commit()
    return post

def test_update_post(authorized_client, test_posts):
    data = {
        "title": "Updated Title",
        "content": "Updated Content"
    }
    post_id = test_posts[0].id
    response = authorized_client.put(f"/posts/{post_id}", json=data)

    assert response.status_code == 200
    updated_post = response.json()
    assert updated_post["title"] == data["title"]
    assert updated_post["content"] == data["content"]


@pytest.fixture
def test_posts(test_user, session):
    posts_data = [
        {"title": "First", "content": "Test 1", "owner_id": test_user["id"]},
        {"title": "Second", "content": "Test 2", "owner_id": test_user["id"]},
    ]
    posts = [models.Post(**post) for post in posts_data]
    session.add_all(posts)
    session.commit()
    return session.query(models.Post).all()

