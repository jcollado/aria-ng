
from loader import Loader

class LiteralLoader(Loader):
    """
    ARIA string loader.
    
    This loader is a trivial holder for the provided string value.
    """

    def __init__(self, value):
        self.value = value
        self.location = '<literal>'
    
    def load(self):
        return str(self.value)
