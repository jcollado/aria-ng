
from .. import AriaError

class ConsumerError(AriaError):
    """
    ARIA consumer error.
    """

class BadImplementationError(ConsumerError):
    """
    ARIA consumer error: bad implementation.
    """
