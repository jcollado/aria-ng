
class Grammar(object):
    """
    Base class for ARIA grammars.
    
    Grammars provide a robust API over agnostic data structures.
    """
    
    def __init__(self, structure={}):
        self.structure = structure
