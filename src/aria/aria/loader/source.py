
from .exceptions import LoaderNotFoundError
from .loader import Loader
from .literal import LiteralLocation, LiteralLoader

class LoaderSource(object):
    """
    Base class for ARIA loader sources.
    
    Loader sources provide appropriate :class:`Loader` instances for locations.
    """
    
    def get_loader(self, location, origin_location):
        if isinstance(location, LiteralLocation):
            return LiteralLoader(location.value)
        raise LoaderNotFoundError(location)
