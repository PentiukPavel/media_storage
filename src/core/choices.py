from enum import StrEnum


class APIExceptions(StrEnum):
    CAN_NOT_GET_AUTH_CODE = "Не удалось получить url для авторизации."
    CAN_NOT_GET_AUTH_TOKEN = "Не удалось получить токен авторизации."
    CAN_NOT_GET_USER_INFO = "Не удалось получить данные пользователя."

    FILENAME_EXISTS = "Файл с таким именем уже существует."
