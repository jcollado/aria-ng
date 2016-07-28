
from ..utils import LockedList

class ReadingContext(object):
    def __init__(self):
        self.locations = LockedList()
