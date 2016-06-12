
from aria import UnimplementedFunctionalityError, classname

class Loader(object):
    """
    Base class for ARIA loaders.
    
    Loaders extract data by consuming a data source.
    
    Though the extracted data is often textual (a string or string-like
    data), loaders may provide any format.
    """
    
    def load(self):
        raise UnimplementedFunctionalityError(classname(self) + '.read')
    
    def open(self):
        pass

    def close(self):
        pass
