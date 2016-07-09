
from .. import UnimplementedFunctionalityError, classname

class Loader(object):
    """
    Base class for ARIA loaders.
    
    Loaders extract a document by consuming a document source.
    
    Though the extracted document is often textual (a string or string-like
    data), loaders may provide any format.
    """
    
    def load(self):
        raise UnimplementedFunctionalityError(classname(self) + '.load')
    
    def open(self):
        pass

    def close(self):
        pass
