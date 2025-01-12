

__all__ = ['PlayerNotFoundError', 'RecordNotFoundError']

from typing import Literal


class NotFoundError(Exception):
    def __init__(self, error_type: str, message: str = "Player not found"):
        super().__init__(message)

class PlayerNotFoundError(NotFoundError):
    """
    Raised when a player cannot be found.
    """
    def __init__(self, error_type: str, message: str = "No player found"):
        super().__init__(error_type,message)
        self.message = message
        self.error_type = error_type

class RecordNotFoundError(NotFoundError):
    """
    Raised when a recent record cannot be found.
    """
    def __init__(self,  error_type: str, message: str = "Recent record does not exist"):
        super().__init__(error_type, message)
        self.message = message
        self.error_type = error_type
