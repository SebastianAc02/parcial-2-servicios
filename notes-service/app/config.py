import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-me')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///notes.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
