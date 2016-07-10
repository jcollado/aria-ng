
from .. import AriaError, Issue

class ReaderError(AriaError):
    """
    ARIA reader error.
    """

    def __init__(self, message, cause=None, cause_tb=None, location=None, line=None, column=None, map=None, snippet=None):
        super(ReaderError, self).__init__(message, cause, cause_tb)
        self.issue = Issue(message, location=location, line=line, column=column, map=map, snippet=snippet)

class ReaderNotFoundError(ReaderError):
    """
    ARIA reader error: reader not found for source.
    """
