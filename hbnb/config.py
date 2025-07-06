import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
