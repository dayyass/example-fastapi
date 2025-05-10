import pytest

from app import schemas


def test_get_all_posts(autorized_client, test_posts):
    res = autorized_client.get("/posts/")
    assert res.status_code == 200

    posts = [schemas.PostOut(**post) for post in res.json()]
    assert len(posts) == len(test_posts)


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(autorized_client, test_posts):
    res = autorized_client.get("/posts/99999")
    assert res.status_code == 404


def test_get_one_post(autorized_client, test_posts):
    res = autorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200

    post = schemas.PostOut(**res.json())
    assert post.post.id == test_posts[0].id
    assert post.post.title == test_posts[0].title
    assert post.post.content == test_posts[0].content
    assert post.post.owner_id == test_posts[0].owner_id


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(autorized_client, test_user, test_posts, title, content, published):
    res = autorized_client.post(
        "/posts/",
        json={
            "title": title,
            "content": content,
            "published": published,
        }
    )
    assert res.status_code == 201

    created_post = schemas.Post(**res.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]


def test_create_post_default_published(autorized_client, test_user, test_posts):
    res = autorized_client.post(
        "/posts/",
        json={
            "title": "awesome new title",
            "content": "awesome new content",
        }
    )
    assert res.status_code == 201

    created_post = schemas.Post(**res.json())
    assert created_post.title == "awesome new title"
    assert created_post.content == "awesome new content"
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]


def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post(
        "/posts/",
        json={
            "title": "awesome new title",
            "content": "awesome new content",
        }
    )
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(autorized_client, test_user, test_posts):
    res = autorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_not_exist(autorized_client, test_user, test_posts):
    res = autorized_client.delete("/posts/99999")
    assert res.status_code == 404


def test_delete_other_user_post(autorized_client, test_user, test_posts):
    res = autorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(autorized_client, test_user, test_posts):
    updated_data = {
        "title": "updated title",
        "content": "updated content",
    }
    res = autorized_client.put(
        f"/posts/{test_posts[0].id}",
        json=updated_data,
    )
    assert res.status_code == 200

    updated_post = schemas.Post(**res.json())
    assert updated_post.title == updated_data["title"]
    assert updated_post.content == updated_data["content"]


def test_update_other_user_post(autorized_client, test_user, test_user2, test_posts):
    updated_data = {
        "title": "updated title",
        "content": "updated content",
    }
    res = autorized_client.put(
        f"/posts/{test_posts[3].id}",
        json=updated_data,
    )
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    updated_data = {
        "title": "updated title",
        "content": "updated content",
    }
    res = client.put(
        f"/posts/{test_posts[0].id}",
        json=updated_data,
    )
    assert res.status_code == 401


def test_update_post_not_exist(autorized_client, test_user, test_posts):
    updated_data = {
        "title": "updated title",
        "content": "updated content",
    }
    res = autorized_client.put(
        "/posts/99999",
        json=updated_data,
    )
    assert res.status_code == 404
