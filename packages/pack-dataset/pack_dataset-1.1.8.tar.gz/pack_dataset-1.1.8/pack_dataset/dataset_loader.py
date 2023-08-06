import os
import pymssql
import pandas as pd
from .custom_exception import *
import hvac
import json


class GetterData:
    """
    Основной класс обработчик и загрузчик данных
    """

    def __init__(self):
        self.connection = None
        self.connect_data = self.get_connect_data()
        self.self_path = os.path.abspath(os.curdir)
        try:
            self.settings = self.read_settings()
        except Exception:
            print('Неудалось найти настроечный файл, пожалуйста создайте его прежде чем начать работу!')

    def read_settings(self):
        """
        Функция чтения файла настройки
        Returns
        ---------
            settings: dict
                Словарь содержащий в себе компоненты необходимые для выгрузки данных
        """
        with open(os.path.join(self.self_path, "settings.json"), 'r') as file:
            settings = json.load(file)
        return settings

    def write_secret_token_settings(self, prefix_login='', url='', cert_vault_tls='', cert_vault_key='',
                                    cert_vault_verify='', vault_token='', vault_secret_engine='',
                                    vault_path=''):
        """
        Функция создания файла настроек с сикретным токеном

        Parameters
        ------------
            prefix_login: str
                Префикс для логина (если не требуется добавьте поле и передайте пустую строку)
            url: str
                Url для подключения с использованием секретного токена
            cert_vault_tls: str
                Путь до секретного сертификата
            cert_vault_key: str
                Путь до ключа сертификата
            cert_vault_verify: str
                Путь до верификации сертификата
            vault_token: str
                Vault токен
            vault_secret_engine: str
                Названиие используемого Secret Engine
            vault_path: str
                Путь до секрета в Vault
        """
        settings_to_json = {'prefix_login': prefix_login,
                            'url': url,
                            'cert_vault_tls': cert_vault_tls,
                            'cert_vault_key': cert_vault_key,
                            'cert_vault_verify': cert_vault_verify,
                            'vault_token': vault_token,
                            'vault_secret_engine': vault_secret_engine,
                            'vault_path': vault_path, }

        with open((os.path.join(self.self_path, "settings.json")), 'w') as file:
            json.dump(settings_to_json, file)

    def write_login_settings(self, prefix_login='', login='', password=''):
        """
        Функция создания файла настроек с логином и паролем

        Parameters
        ------------
            prefix_login: str
                Префикс для логина (если не требуется добавьте поле и передайте пустую строку)
            login: str
                Логин пользователя
            password: str
                Пароль пользователя
        """
        settings_to_json = {'prefix_login': prefix_login,
                            'login': login,
                            'password': password, }

        with open((os.path.join(self.self_path, "settings.json")), 'w') as file:
            json.dump(settings_to_json, file)

    def get_connect_data(self):
        """
        Функция для получения данных для подключения к базе
        Returns
        ---------
            connect_data: dict
                Словарь содержащий данные для подключения к базе данных
        """
        connect_data = {}
        try:
            connect_data_raw = os.environ.get(
                filter(lambda x: x.startswith("DATASET") and x.endswith("PATH"), os.environ).__next__())
            for pair in connect_data_raw.split(";")[:-1]:
                k, v = pair.split("=")
                connect_data[k.lower()] = v
        except Exception:
            print("Не удалось считать данные для подключения в автоматическом режиме, введите их пожалуйста вручную!")
        return connect_data

    def connect_to_db_with_login(self):
        """
        Функция для подключения к базе данных с использованием логином и пароля
        Raises
        -------------
            ConnectException
                Исключение, вызываемое при отсутствии данных для подключения к базе (сервер, база данных, схема, таблица)
        """
        if "login" in self.settings.keys() and "password" in self.settings.keys():
            self.connect_data['username'] = self.settings['prefix_login'].replace('/', '\\') + self.settings['login']
            self.connect_data['password'] = self.settings['password']
            self.connection = pymssql.connect(self.connect_data["server"],
                                              self.connect_data["username"],
                                              self.connect_data["password"],
                                              self.connect_data["database"])
        else:
            raise ConnectExceptionLogin

    def connect_to_db_with_token(self):
        """
        Функция для подключения к базе данных с использованием библиотеки hvac

        Raises
        -------------
            ConnectException
                Исключение, вызываемое при отсутствии данных для подключения к базе (сервер, база данных, схема, таблица)
        """
        if "url" in self.settings.keys() and "cert_vault_tls" in self.settings.keys() and \
                "cert_vault_key" in self.settings.keys() and "cert_vault_verify" in self.settings.keys():

            cli = hvac.Client(url=self.settings['url'],
                              token=self.settings['vault_token'],
                              cert=(self.settings["cert_vault_tls"], self.settings["cert_vault_key"]),
                              verify=self.settings["cert_vault_verify"])
            if cli.is_authenticated():
                creds = cli.secrets.kv.v2.read_secret_version(mount_point=self.settings['vault_secret_engine'],
                                                              path=self.settings['vault_path']).get("data").get("data")

                login = creds.get('username')
                password = creds.get('password')
                self.connect_data['username'] = self.settings['prefix_login'].replace('/', '\\') + login
                self.connect_data['password'] = password
                self.connection = pymssql.connect(self.connect_data["server"],
                                                  self.connect_data["username"],
                                                  self.connect_data["password"],
                                                  self.connect_data["database"])
        else:
            raise ConnectExceptionToken

    def get_data_weather(self, row=None):
        """
        Функция для получения набора данных погоды (не указывай ничего если необходимо выгрузить весь набор данных)

        Parameters
        ------------
            row: int
                Число строк в выгружаемом наборе данных
        Raises
        -------------
            ConnectException
                Исключение, вызываемое при несоответствии параметра строки на целочисленное число
        """
        if (row is not None) and (type(row) == int) and (row > 0):
            sql_query = f"SELECT TOP {row} * FROM [{self.connect_data['database']}].[{self.connect_data['schema']}].[{self.connect_data['table']}]"
        elif type(row) != int or row < 0:
            raise RowException
        else:
            # Пока 35к как потолок, иначе кернел валится
            sql_query = f"SELECT TOP 35000 * FROM [{self.connect_data['database']}].[{self.connect_data['schema']}].[{self.connect_data['table']}]"
        dataset = pd.read_sql(sql_query, self.connection)
        return dataset
