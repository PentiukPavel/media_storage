from enum import IntEnum


class Limit(IntEnum):
    """
    Предельные значения.
    """

    MAX_LENGTH_FILENAME = 100
    MAX_FILE_SIZE_MB = 2 * 1024 * 1024
