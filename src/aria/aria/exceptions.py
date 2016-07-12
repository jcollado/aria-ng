
from .issue import Issue
import sys

class AriaError(Exception):
    """
    Base class for ARIA errors.
    """
    
    def __init__(self, message=None, cause=None, cause_tb=None):
        super(AriaError, self).__init__(message)
        self.cause = cause
        if cause_tb is None:
            _, e, tb = sys.exc_info()
            if cause == e:
                # Make sure it's our traceback
                cause_tb = tb
        self.cause_tb = cause_tb

class UnimplementedFunctionalityError(AriaError):
    """
    ARIA error: functionality is unimplemented.
    """

class InvalidValueError(AriaError):
    """
    ARIA error: value is invalid.
    """

    def __init__(self, message, cause=None, cause_tb=None, location=None, line=None, column=None, locator=None, snippet=None):
        super(InvalidValueError, self).__init__(message, cause, cause_tb)
        self.issue = Issue(message, location=location, line=line, column=column, locator=locator, snippet=snippet)
