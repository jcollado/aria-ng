
class AriaError(Exception):
    """
    Base class for ARIA errors.
    """
    
    def __init__(self, message, cause=None):
        super(AriaError, self).__init__(str(message))
        self.cause = cause

class UnimplementedAriaError(AriaError):
    """
    ARIA error: funcionality is unimplemented.
    """

class OpenClose(object):
    """
    Wraps an object that has open() and close() methods to support the "with" keyword.
    """
    
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __enter__(self):
        if hasattr(self.wrapped, 'open'):
            self.wrapped.open()
        return self.wrapped

    def __exit__(self, type, value, traceback):
        if hasattr(self.wrapped, 'close'):
            self.wrapped.close()
        return False

def classname(o):
    return o.__module__ + '.' + o.__class__.__name__
