class ExternalServiceError(Exception):
    pass


class ExternalService:

    def __init__(self, client):
        self.client = client

    def get_users(self):
        try:
            return self.client.get_users()
        except Exception:
            raise ExternalServiceError('External service unavailable')

    def get_posts(self):
        try:
            return self.client.get_posts()
        except Exception:
            raise ExternalServiceError('External service unavailable')

    def get_posts_by_user(self, user_id):
        try:
            return self.client.get_posts_by_user(user_id)
        except Exception:
            raise ExternalServiceError('External service unavailable')
