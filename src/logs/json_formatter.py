import datetime
import json
import logging
import os
import traceback

from core.config import settings
from logs.schemes import BaseJsonLogSchema


LEVEL_TO_NAME = {
    10: "DEBUG",
    20: "INFO",
    30: "WARNING",
    40: "ERROR",
    50: "CRITICAL",
}


class JSONLogFormatter(logging.Formatter):
    """
    Кастомизированный класс-форматер для логов в формате json
    """

    def format(self, record: logging.LogRecord, *args, **kwargs) -> str:
        """
        Преобразование объект журнала в json
        :param record: объект журнала
        :return: строка журнала в JSON формате
        """

        log_object: dict = self._format_log_object(record)
        return json.dumps(log_object, ensure_ascii=False)

    @staticmethod
    def _format_log_object(record: logging.LogRecord) -> dict:
        """
        Перевод записи объекта журнала
        в json формат с необходимым перечнем полей
        :param record: объект журнала
        :return: Словарь с объектами журнала
        """

        now = (
            datetime.datetime.fromtimestamp(record.created)
            .astimezone()
            .replace(microsecond=0)
            .isoformat()
        )
        message = record.getMessage()
        duration = (
            record.duration if hasattr(record, "duration") else record.msecs
        )
        json_log_fields = BaseJsonLogSchema(
            thread=record.process,
            timestamp=now,
            level=record.levelno,
            level_name=LEVEL_TO_NAME[record.levelno],
            message=message,
            source=record.name,
            duration=duration,
        )

        if hasattr(record, "props"):
            json_log_fields.props = record.props

        if record.exc_info:
            json_log_fields.exceptions = traceback.format_exception(
                *record.exc_info
            )

        elif record.exc_text:
            json_log_fields.exceptions = record.exc_text
        json_log_object = json_log_fields.model_dump(
            exclude_unset=True,
            by_alias=True,
        )
        if hasattr(record, "request_json_fields"):
            json_log_object.update(record.request_json_fields)

        return json_log_object


def write_log(msg):
    parsed = json.loads(msg)
    print(json.dumps(parsed, indent=4))


def write_file(msg):
    if not os.path.exists(settings.ERROR_LOG_FILENAME):
        with open(settings.ERROR_LOG_FILENAME, "w") as log_file:
            data = []
            json.dump(data, log_file)
    with open(settings.ERROR_LOG_FILENAME, "r") as log_file:
        data = json.load(log_file)
        message = json.loads(msg)
        message_dict = {}
        message_dict[datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")] = (
            message
        )
        data.append(message_dict)
    with open(settings.ERROR_LOG_FILENAME, "w") as file:
        json.dump(data, file, indent=4)
