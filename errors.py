class MiniFSError(Exception):
    """Base class for all mini FS errors."""

class InvalidPathError(MiniFSError):
    pass

class InvalidNameError(MiniFSError):
    pass

class NotFoundError(MiniFSError):
    pass

class AlreadyExistsError(MiniFSError):
    pass

class NotADirectoryError(MiniFSError):
    pass

class NotAFileError(MiniFSError):
    pass

class DirectoryNotEmptyError(MiniFSError):
    pass
