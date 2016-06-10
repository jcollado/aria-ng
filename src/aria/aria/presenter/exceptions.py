
from aria import AriaError

class PresenterError(AriaError):
    """
    ARIA presenter error.
    """
    pass

class PresenterNotFoundPresenterError(PresenterError):
    """
    ARIA presenter error: presenter not found for raw.
    """
    pass
