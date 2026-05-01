import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-me')
    JSONPLACEHOLDER_BASE_URL = 'https://jsonplaceholder.typicode.com'
    EXTERNAL_API_TIMEOUT = 5
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
