class NotFoundError(Exception):
    """Generic not found exception."""
    
    def __init__(self, message="Resource not found"):
        self.message = message
        super().__init__()

class AlreadyExistsError(Exception):
    """Exception raised when trying to add a resource that already exists."""
    def __init__(self, message="Resource already exists"):
        self.message = message
        super().__init__()
