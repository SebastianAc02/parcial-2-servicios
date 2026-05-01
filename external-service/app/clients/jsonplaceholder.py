import requests


class JsonPlaceholderClient:

    def __init__(self, base_url, timeout):
        self.base_url = base_url
        self.timeout = timeout

    def get_users(self):
        resp = requests.get(f'{self.base_url}/users', timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def get_posts(self):
        resp = requests.get(f'{self.base_url}/posts', timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def get_posts_by_user(self, user_id):
        resp = requests.get(
            f'{self.base_url}/posts',
            params={'userId': user_id},
            timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()
