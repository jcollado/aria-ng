
from .. import AriaError

class PresenterError(AriaError):
    """
    ARIA presenter error.
    """

class PresenterNotFoundError(PresenterError):
    """
    ARIA presenter error: presenter not found for raw.
    """
