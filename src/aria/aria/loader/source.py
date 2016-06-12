
from exceptions import LoaderNotFoundError
from loader import Loader

class LoaderSource(object):
    """
    Base class for ARIA loader sources.
    
    Loader sources provide appropriate :class:`Loader` instances for locators.
    """
    
    def get_loader(self, locator, origin_locator):
        if isinstance(locator, Loader):
            return locator
        elif isinstance(locator, basestring):
            return LiteralLoader(locator)
        raise LoaderNotFoundError(locator)
