class MovieAlreadyExistsError(Exception):
    """Exception raised when trying to add a movie that already exists."""
    pass

class MovieNotFoundError(Exception):
    """Exception raised when a movie is not found in the database."""
    pass