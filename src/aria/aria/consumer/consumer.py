from aria import UnimplementedFunctionalityError, classname

class Consumer(object):
    """
    
    Base class for ARIA consumers.
    
    Consumers provide useful functionality by consuming presentations.
    
    """
    
    def __init__(self, presentation, args=[]):
        self.presentation = presentation
        self.args = args
    
    def consume(self):
        raise UnimplementedFunctionalityError(classname(self) + '.consume')
