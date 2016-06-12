
from exceptions import PresenterNotFoundError

class PresenterSource(object):
    """
    Base class for ARIA presenter sources.
    
    Presenter sources provide appropriate :class:`Presenter` classes for agnostic raw data.
    """

    def get_presenter(self, raw):
        raise PresenterNotFoundError()
