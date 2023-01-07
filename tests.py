from unittest import TestCase

from flask_migrate import upgrade

from app import app


TEST_USERNAME = "test_user"
TEST_PASSWORD = "test_password"


class TestUser(TestCase):

    def setUp(self) -> None:
        with app.app_context():
            upgrade()

    def test_post_blog(self):
        client = app.test_client()

        user_data = {
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD,
        }

        response = client.post("/users", json=user_data)
        assert response.status_code == 200
        assert response.json["status"] == "success"

        response = client.post("/login", json=user_data)
        assert response.status_code == 200
        assert response.json["status"] == "success"

        blog_data = {
            "name": "blogname",
            "description": "Blog Description",
        }
        response = client.post("/blogs", json=blog_data)
        assert response.status_code == 200
        assert response.json["status"] == "success"

        new_blog_id = response.json["new_id"]
        post_data = {
            "title": "TItle 1",
            "text": "Description 1"
        }
        response = client.post(f"/blogs/{new_blog_id}/posts", json=post_data)
        assert response.status_code == 200
        assert response.json["status"] == "success"
        assert response.json["new_id"] > 0

