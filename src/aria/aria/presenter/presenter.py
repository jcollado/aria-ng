
from .. import merge
from .presentation import Presentation

class Presenter(Presentation):
    """
    Base class for ARIA presenters.
    
    Presenters provide a robust API over agnostic raw data.
    """
    
    def __init__(self, raw={}):
        self.raw = raw

    def merge_import(self, presentation):
        merge(self.raw, presentation.raw)
        if hasattr(self.raw, '_map') and hasattr(presentation.raw, '_map'):
            self.raw._map.merge(presentation.raw._map)

    def link(self):
        map = self.raw._map
        map.link(self.raw)
