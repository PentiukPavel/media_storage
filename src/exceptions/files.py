from core.choices import APIExceptions


class FilenameExists(Exception):
    def __init__(self):
        message = APIExceptions.FILENAME_EXISTS.value
        super().__init__(message)


class WrongFilename(Exception):
    def __init__(self):
        message = APIExceptions.WRONG_FILENAME.value
        super().__init__(message)
