
from .. import AriaError

class LoaderError(AriaError):
    """
    ARIA loader error.
    """

class LoaderNotFoundError(LoaderError):
    """
    ARIA loader error: loader not found for source.
    """

class DocumentNotFoundError(LoaderError):
    """
    ARIA loader error: document not found.
    """
