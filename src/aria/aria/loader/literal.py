
from .loader import Loader

class LiteralLocation(object):
    def __init__(self, value):
        self.value = value

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
