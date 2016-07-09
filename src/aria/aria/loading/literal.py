
from .loader import Loader

class LiteralLocation(object):
    def __init__(self, value):
        self.value = value

class LiteralLoader(Loader):
    """
    ARIA literal loader.
    
    This loader is a trivial holder for the provided value.
    """

    def __init__(self, value, location='<literal>'):
        self.value = value
        self.location = location
    
    def load(self):
        return self.value
