
class AriaError(Exception):
    """
    Base class for ARIA errors.
    """
    
    def __init__(self, message, cause=None):
        super(AriaError, self).__init__(str(message))
        self.cause = cause

class UnimplementedFunctionalityError(AriaError):
    """
    ARIA error: funcionality is unimplemented.
    """
