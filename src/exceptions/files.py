from core.choices import APIExceptions


class FilenameExists(Exception):
    def __init__(self):
        message = APIExceptions.FILENAME_EXISTS.value
        super().__init__(message)


class WrongFilename(Exception):
    def __init__(self):
        message = APIExceptions.WRONG_FILENAME.value
        super().__init__(message)


class FileIsTooLarge(Exception):
    def __init__(self):
        message = APIExceptions.FILE_IS_TOO_LARGE.value
        super().__init__(message)


class WrongFileType(Exception):
    def __init__(self):
        message = APIExceptions.WRONG_FILE_TYPE.value
        super().__init__(message)
