import pytest
import requests
from unittest.mock import MagicMock, patch
from app.services.external_service import ExternalService, ExternalServiceError


@pytest.fixture
def mock_client():
    return MagicMock()


@pytest.fixture
def service(mock_client):
    return ExternalService(mock_client)


class TestGetUsers:
    def test_get_users_success(self, service, mock_client):
        mock_client.get_users.return_value = [{'id': 1, 'name': 'Alice'}]
        result = service.get_users()
        assert len(result) == 1
        assert result[0]['name'] == 'Alice'

    def test_get_users_timeout_raises(self, service, mock_client):
        mock_client.get_users.side_effect = requests.Timeout
        with pytest.raises(ExternalServiceError):
            service.get_users()

    def test_get_users_connection_error_raises(self, service, mock_client):
        mock_client.get_users.side_effect = requests.ConnectionError
        with pytest.raises(ExternalServiceError):
            service.get_users()


class TestGetPosts:
    def test_get_posts_success(self, service, mock_client):
        mock_client.get_posts.return_value = [{'id': 1, 'title': 'Post 1'}]
        result = service.get_posts()
        assert len(result) == 1

    def test_get_posts_timeout_raises(self, service, mock_client):
        mock_client.get_posts.side_effect = requests.Timeout
        with pytest.raises(ExternalServiceError):
            service.get_posts()


class TestGetPostsByUser:
    def test_get_posts_by_user_success(self, service, mock_client):
        mock_client.get_posts_by_user.return_value = [{'id': 1, 'userId': 5}]
        result = service.get_posts_by_user(5)
        assert result[0]['userId'] == 5
        mock_client.get_posts_by_user.assert_called_once_with(5)

    def test_get_posts_by_user_empty(self, service, mock_client):
        mock_client.get_posts_by_user.return_value = []
        result = service.get_posts_by_user(9999)
        assert result == []

    def test_get_posts_by_user_timeout_raises(self, service, mock_client):
        mock_client.get_posts_by_user.side_effect = requests.Timeout
        with pytest.raises(ExternalServiceError):
            service.get_posts_by_user(1)
