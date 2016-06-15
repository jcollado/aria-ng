
from .. import AriaError

class ReaderError(AriaError):
    """
    ARIA reader error.
    """

class ReaderNotFoundReaderError(ReaderError):
    """
    ARIA reader error: reader not found for source.
    """
