class UserAlreadyExistsError(Exception):
    """El usuario ya existe en la base de datos"""
    pass

class UserNotFoundError(Exception):
    """El usuario no fue encontrado"""
    pass

class InvalidCredentialsError(Exception):
    """Contraseña incorrecta"""
    pass
