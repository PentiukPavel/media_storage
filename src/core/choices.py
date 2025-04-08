from enum import StrEnum

from core.config import settings
from core.limits import Limit


class APIExceptions(StrEnum):
    CAN_NOT_GET_AUTH_CODE = "Не удалось получить url для авторизации."
    CAN_NOT_GET_AUTH_TOKEN = "Не удалось получить токен авторизации."
    CAN_NOT_GET_USER_INFO = "Не удалось получить данные пользователя."

    FILENAME_EXISTS = "Файл с таким именем уже существует."
    WRONG_FILENAME = (
        "Длинна имени файла не должна превышать"
        f" {Limit.MAX_LENGTH_FILENAME.value}."
    )
    FILE_IS_TOO_LARGE = (
        "Размер файла должен быть менше" f" {Limit.MAX_FILE_SIZE_MB.value}."
    )
    WRONG_FILE_TYPE = (
        f"Тип сохраняемого файла должен быть {', '.join(settings.FILE_TYPES)}"
    )
