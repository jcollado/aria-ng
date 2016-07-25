
from .. import AriaError, Issue

class ReaderError(AriaError):
    """
    ARIA reader error.
    """

class ReaderNotFoundError(ReaderError):
    """
    ARIA reader error: reader not found for source.
    """

class SyntaxError(ReaderError):
    """
    ARIA read format error.
    """

    def __init__(self, message, cause=None, cause_tb=None, location=None, line=None, column=None, locator=None, snippet=None, level=Issue.SYNTAX):
        super(ReaderError, self).__init__(message, cause, cause_tb)
        self.issue = Issue(message, location=location, line=line, column=column, locator=locator, snippet=snippet, level=level)

class AlreadyReadError(ReaderError):
    """
    ARIA reader error: already read.
    """
