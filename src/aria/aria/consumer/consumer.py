from aria import UnimplementedAriaError, classname

class Consumer(object):
    """
    
    Base class for ARIA consumers.
    
    Consumers provide useful functionality by consuming presentations.
    
    """
    
    def __init__(self, presentation):
        self.presentation = presentation
    
    def consume(self):
        raise UnimplementedAriaError(classname(self) + '.consume')
