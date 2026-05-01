import pytest
from unittest.mock import patch, MagicMock
from app import create_app
import requests


@pytest.fixture
def app():
    app = create_app(testing=True)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


class TestGetUsers:
    def test_get_users_success(self, client):
        mock_users = [{'id': 1, 'name': 'Alice', 'email': 'alice@test.com'}]
        with patch('app.clients.jsonplaceholder.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_users
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            response = client.get('/external/users')
        assert response.status_code == 200
        assert len(response.get_json()) == 1

    def test_get_users_service_unavailable(self, client):
        with patch('app.clients.jsonplaceholder.requests.get') as mock_get:
            mock_get.side_effect = requests.Timeout
            response = client.get('/external/users')
        assert response.status_code == 503
        assert 'error' in response.get_json()


class TestGetPosts:
    def test_get_posts_success(self, client):
        mock_posts = [{'id': 1, 'title': 'Post 1', 'userId': 1}]
        with patch('app.clients.jsonplaceholder.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_posts
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            response = client.get('/external/posts')
        assert response.status_code == 200
        assert len(response.get_json()) == 1

    def test_get_posts_service_unavailable(self, client):
        with patch('app.clients.jsonplaceholder.requests.get') as mock_get:
            mock_get.side_effect = requests.ConnectionError
            response = client.get('/external/posts')
        assert response.status_code == 503


class TestGetPostsByUser:
    def test_get_posts_by_user_success(self, client):
        mock_posts = [{'id': 1, 'userId': 3, 'title': 'My Post'}]
        with patch('app.clients.jsonplaceholder.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_posts
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            response = client.get('/external/posts/3')
        assert response.status_code == 200
        data = response.get_json()
        assert data[0]['userId'] == 3

    def test_get_posts_by_user_empty(self, client):
        with patch('app.clients.jsonplaceholder.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = []
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            response = client.get('/external/posts/9999')
        assert response.status_code == 200
        assert response.get_json() == []

    def test_get_posts_by_user_timeout(self, client):
        with patch('app.clients.jsonplaceholder.requests.get') as mock_get:
            mock_get.side_effect = requests.Timeout
            response = client.get('/external/posts/1')
        assert response.status_code == 503
