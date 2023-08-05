from flask import jsonify


class JsonResponse:
    """
    Класс обертывания ответа сервера в коды состояния.
    """
    HTTP_CODE_OK = 200
    HTTP_CODE_NOT_FOUND = 404

    def success(self, data: dict = None):
        """
        Метод обертывания ответа сервера в статус-код 200.

        :param data: ответ сервера
        :type data: dict
        :return: ответ сервера
        """
        return self._response(self.HTTP_CODE_OK, data)

    def not_found(self, data: dict = None):
        """
        Метод обертывания ответа сервера в статус-код 404.

        :param data: ответ сервера
        :type data: dict
        :return: ответ сервера
        """
        return self._response(self.HTTP_CODE_NOT_FOUND, data)

    @classmethod
    def _response(cls, code: int, data: dict = None):
        """
        Метод оборачивания ответа сервера в json.

        :param code: статус-код
        :param data: ответ сервера
        :return: обёрнутый ответ сервера
        """
        if data is not None:
            return jsonify(data), code
        return '', code


json_response = JsonResponse()
