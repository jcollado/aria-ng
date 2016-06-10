
class Presenter(object):
    """
    Base class for ARIA presenters.
    
    Presenters provide a robust API over agnostic raw data.
    """
    
    def __init__(self, raw={}):
        self.raw = raw
