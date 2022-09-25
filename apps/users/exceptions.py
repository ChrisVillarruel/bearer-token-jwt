class UserException(Exception):
    def __init__(self, code_error: int):
        self.code_error = code_error


class UserValidationException(UserException):
    """ Todas las validaciones de usuario """


class UserAthorizationException(UserException):
    """ Todas las validaciones cuando un usuario de authentica """
