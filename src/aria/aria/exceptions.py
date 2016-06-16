
import sys

class AriaError(Exception):
    """
    Base class for ARIA errors.
    """
    
    def __init__(self, message, cause=None, cause_tb=None):
        super(AriaError, self).__init__(str(message))
        self.cause = cause
        if cause_tb is None:
            _, e, tb = sys.exc_info()
            if cause == e:
                # Make sure it's our traceback
                cause_tb = tb
        self.cause_tb = cause_tb

class UnimplementedFunctionalityError(AriaError):
    """
    ARIA error: funcionality is unimplemented.
    """

class InvalidValueError(AriaError):
    """
    ARIA error: value is invalid.
    """
