class MovieAlreadyExistsError(Exception):
    """Exception raised when trying to add a movie that already exists."""
    pass

class MovieNotFoundError(Exception):
    """Exception raised when a movie is not found in the database."""
    pass

class ActorAlreadyExistsError(Exception):
    """Exception raised when trying to add an actor that already exists."""
    pass

class ActorNotFoundError(Exception):
    """Exception raised when an actor is not found in the database."""
    pass