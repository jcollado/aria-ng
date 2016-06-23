
from .. import AriaError

class ExecutorError(AriaError):
    """
    ARIA executor error.
    """

class ExecutorNotFoundError(ExecutorError):
    """
    ARIA executor not found error.
    """
