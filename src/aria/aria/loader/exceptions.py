
from .. import AriaError

class LoaderError(AriaError):
    """
    ARIA loader error.
    """

class LoaderNotFoundError(LoaderError):
    """
    ARIA loader error: loader not found for source.
    """

class SourceNotFoundError(LoaderError):
    """
    ARIA loader error: resource not found.
    """
