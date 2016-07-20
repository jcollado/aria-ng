
from .. import UnimplementedFunctionalityError, OpenClose, classname
from .exceptions import ReaderError

class Reader(object):
    """
    Base class for ARIA readers.
    
    Readers provide agnostic raw data by consuming :class:`aria.loader.Loader` instances.
    """
    
    def __init__(self, source, location, loader):
        self.source = source
        self.location = location
        self.loader = loader

    def load(self):
        with OpenClose(self.loader) as loader:
            data = loader.load()
            if data is None:
                raise ReaderError('loader did not provide data: %s' % self.loader)
            self.location = loader.location # loader may change the location during loading
            return data
    
    def read(self):
        raise UnimplementedFunctionalityError(classname(self) + '.read')
