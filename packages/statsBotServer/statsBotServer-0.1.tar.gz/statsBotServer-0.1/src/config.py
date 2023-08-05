import os


class Config:
    """ Класс с конфигурацией для FLASK приложения. """
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = os.getenv('DEBUG', True)
    DB_CONNECTION = os.getenv('DB_CONNECTION', 'db.sqlite')
    SECRET_KEY = os.getenv('SECRET_KEY', '4f4g5sdew98vsef1t2a5v7b').encode()
