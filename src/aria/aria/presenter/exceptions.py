
from aria import AriaError

class PresenterError(AriaError):
    """
    ARIA presenter error.
    """
    pass

class PresenterNotFoundError(PresenterError):
    """
    ARIA presenter error: presenter not found for raw.
    """
    pass
