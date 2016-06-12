
from aria import AriaError

class LoaderError(AriaError):
    """
    ARIA loader error.
    """
    pass

class LoaderNotFoundError(LoaderError):
    """
    ARIA loader error: loader not found for source.
    """
    pass

class SourceNotFoundError(LoaderError):
    """
    ARIA loader error: resource not found.
    """
    pass
