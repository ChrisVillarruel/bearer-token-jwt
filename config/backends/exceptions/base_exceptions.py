class BaseExceptionProject(Exception):
    def __init__(self, code_error: int):
        self.code_error = code_error


class BaseAthorizationException(BaseExceptionProject):
    """ Todas las validaciones cuando un usuario de authentica """
