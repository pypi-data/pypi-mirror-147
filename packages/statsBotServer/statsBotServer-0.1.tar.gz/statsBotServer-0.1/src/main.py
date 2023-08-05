"""
Модуль старта приложения.
"""
from flask import Flask
from views.stats_acquisition import acquisition_bp


def create_app():
    """
    Метод создания Flask приложения.
    :return: приложение Flask
    """
    app = Flask(__name__)  # Создание приложения Flask.
    app.debug=True
    app.config.from_object('config.Config')  # Проброс конфигурационных параметров.
    app.register_blueprint(acquisition_bp, url_prefix='/acquisition')

    return app
