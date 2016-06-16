
from .exceptions import ReaderNotFoundReaderError

class ReaderSource(object):
    """
    Base class for ARIA reader sources.
    
    Reader sources provide appropriate :class:`Reader` instances for locations.
    """

    def get_reader(self, location, loader):
        raise ReaderNotFoundReaderError(location)
