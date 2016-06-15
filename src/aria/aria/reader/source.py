
from .exceptions import ReaderNotFoundReaderError

class ReaderSource(object):
    """
    Base class for ARIA reader sources.
    
    Reader sources provide appropriate :class:`Reader` instances for locators.
    """

    def get_reader(self, locator, loader):
        raise ReaderNotFoundReaderError(locator)
