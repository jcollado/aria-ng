
from aria import UnimplementedFunctionalityError, OpenClose, classname

class Reader(object):
    """
    Base class for ARIA readers.
    
    Readers provide agnostic raw data by consuming :class:`aria.loader.Loader` instances.
    """
    
    def __init__(self, loader):
        self.loader = loader

    def load(self):
        with OpenClose(self.loader) as loader:
            return loader.load()
    
    def read(self):
        raise UnimplementedFunctionalityError(classname(self) + '.read')
