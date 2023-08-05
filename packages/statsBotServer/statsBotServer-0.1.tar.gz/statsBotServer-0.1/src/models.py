import sqlalchemy as db
from sqlalchemy import func


class StatsModel:
    """
    Класс для работы с БД.
    """
    def __init__(self):
        self.engine = db.create_engine('sqlite:///scrapy_forum.db')
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()
        self.forum = db.Table('forum', self.metadata, autoload=True, autoload_with=self.engine)

    # print(forum.columns.keys()) # заголовки столбцов

    def get_number_of_messages_one_user(self, username):
        """
        Метод для получения количества сообщений конкретного пользователя.
        :param username: имя пользователя
        :return: ответ сервера
        """
        query = db.select([func.count()]).where(self.forum.columns.username == username)
        result = self.connection.execute(query).fetchone()
        return result[0]

    def get_number_of_character_one_user(self, username):
        """
        Метод для получения количества символов во всех сообщениях пользователя.
        :param username: имя пользователя
        :return: ответ сервера
        """
        query = db.select([func.length(self.forum.columns.user_message)]).\
            where(self.forum.columns.username == username)
        result = self.connection.execute(query).fetchall()
        number_of_characters = 0
        for number in result:
            number_of_characters += number[0]
        return number_of_characters

    def get_number_of_users(self):
        """
        Метод для получения количества пользователей.
        :return: ответ сервера
        """
        query = db.select([self.forum.columns.username]).group_by(self.forum.columns.username)
        result = self.connection.execute(query).fetchall()
        # print(result) список пользователей
        return len(result)

    def get_number_of_messages_all_users(self):
        """
        Метод для получения количества сообщений всех пользователей.
        :return: ответ сервера
        """
        query = db.select([func.count(self.forum.columns.username)])
        result = self.connection.execute(query).fetchone()
        return result[0]

    def get_number_messages_of_each_user(self):
        """
        Метод для получения количества сообщений каждого пользователя.
        :return: ответ сервера
        """
        query = db.select([self.forum.columns.username, func.count()]).\
            group_by(self.forum.columns.username)
        result = self.connection.execute(query).fetchall()
        return result

    def get_character_count_of_each_user(self):
        """
        Метод для получения количества символов по сообщениям пользователя для всех пользователей.
        :return: ответ сервера
        """
        cte_query = db.select([self.forum.columns.username.label('username'),
                               func.length(self.forum.columns.user_message).
                              label('message_length')]).\
            group_by(self.forum.columns.username, self.forum.columns.user_message)
        cte_query = cte_query.cte('all_messages')
        query2 = db.select(cte_query.c.username, func.sum(cte_query.c.message_length)).\
            group_by(cte_query.c.username)
        result = self.connection.execute(query2).fetchall()
        return result

    def get_users_list(self):
        """
        Метод для получения списка пользователей.
        :return: ответ сервера
        """
        query = query = db.select([func.distinct(self.forum.columns.username)])
        result = self.connection.execute(query).fetchall()
        data = []
        for element in result:
            data.append(element[0])
        return data
