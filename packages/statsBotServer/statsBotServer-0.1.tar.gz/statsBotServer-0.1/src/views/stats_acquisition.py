"""
Модуль класса представления для работы с данными о пользователях.
"""
from flask import Blueprint
import requests
from flask.views import MethodView
from src.utils.response import json_response
from src.models import StatsModel


acquisition_bp = Blueprint('stats_acquisition', __name__)


class StatsAcquisitionView(MethodView):
    """
    Класс представления для работы с общими данными о пользователях.
    """
    def __init__(self):
        self.model = StatsModel()

    def get(self, info_type):
        """
        Метод получения общих данных.
        :param type: тип запрашиваемых данных
        :return: полученные от сервера данные, обернутые в статус-код
        """
        try:
            if info_type == 1:
                data = self.model.get_number_of_users()
            elif info_type == 2:
                data = self.model.get_number_of_messages_all_users()
            elif info_type == 3:
                data = dict(self.model.get_number_messages_of_each_user())
            elif info_type == 4:
                data = dict(self.model.get_character_count_of_each_user())
        except requests.exceptions.RequestException:
            return json_response.not_found()
        return json_response.success(data)


class StatAcquisitionView(MethodView):
    """
    Класс представления для получения данных о конкретном пользователе.
    """
    def __init__(self):
        self.model = StatsModel()

    def get(self, username, info_type):
        """
        Метод получения статистики пользователя.
        :param username: имя пользователя
        :param type: тип запрашиваемых данных
        :return: полученные от сервера данные, обернутые в статус-код
        """
        try:
            if info_type == 1:
                data = self.model.get_number_of_messages_one_user(username)
            elif info_type == 2:
                data = self.model.get_number_of_character_one_user(username)
        except requests.exceptions.RequestException:
            return json_response.not_found()
        return json_response.success(data)


class UsersListAcquisitionView(MethodView):
    """
    Класс представления для получения списка пользователей.
    """
    def __init__(self):
        self.model = StatsModel()

    def get(self):
        """
        Метод получения списка пользователей.
        :return: полученные от сервера данные, обернутые в статус-код
        """
        data = {}
        try:
            data = self.model.get_users_list()
        except requests.exceptions.RequestException:
            return json_response.not_found(data)
        return json_response.success(data)

acquisition_bp.add_url_rule('/<int:info_type>/',
                            view_func=StatsAcquisitionView.as_view('stats_acquisition_view'))
acquisition_bp.add_url_rule('/<username>/<int:info_type>/',
                            view_func=StatAcquisitionView.as_view('stat_acquisition_view'))
acquisition_bp.add_url_rule('', view_func=UsersListAcquisitionView.
                            as_view('users_list_acquisition_view'))
