
from aria import AriaError

class LoaderError(AriaError):
    """
    ARIA loader error.
    """
    pass

class LoaderNotFoundLoaderError(LoaderError):
    """
    ARIA loader error: loader not found for source.
    """
    pass

class SourceNotFoundLoaderError(LoaderError):
    """
    ARIA loader error: resource not found.
    """
    pass
