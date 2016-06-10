
from loader import Loader

class StringLoader(Loader):
    """
    ARIA string loader.
    
    This loader is a trivial holder for the provided string value.
    """

    def __init__(self, value):
        self.value = value
    
    def consume(self):
        return str(self.value)
