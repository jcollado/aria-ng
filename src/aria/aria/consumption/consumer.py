from .. import UnimplementedFunctionalityError, classname

class Consumer(object):
    """
    
    Base class for ARIA consumers.
    
    Consumers provide useful functionality by consuming presentations.
    
    """
    
    def __init__(self, context):
        self.context = context
    
    def consume(self):
        raise UnimplementedFunctionalityError(classname(self) + '.consume')
