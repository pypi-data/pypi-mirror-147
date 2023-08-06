class RowException(Exception):

    def __init__(self):
        self.message_error = 'Укажите пожалуйста колличество строк, как целое положительное число!'

    def __str__(self):
        return self.message_error


class ConnectExceptionLogin(Exception):

    def __init__(self):
        self.message_error = 'Для подключения укажите корректно логин и пароль пользователя!'

    def __str__(self):
        return self.message_error


class ConnectExceptionToken(Exception):

    def __init__(self):
        self.message_error = 'Для подключения укажите корректные данные секретного токена!'

    def __str__(self):
        return self.message_error
