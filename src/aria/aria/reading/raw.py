
from .reader import Reader

class RawReader(Reader):
    """
    ARIA raw reader.
    
    Expects to receive agnostic raw data from the loader, and so does nothing to it.
    """
    
    def read(self):
        return self.load()
