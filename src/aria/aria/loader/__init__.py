
from .exceptions import *
from .loader import *
from .source import *
from .literal import *
from .uri import *

import urlparse

class DefaultLoaderSource(LoaderSource):
    """
    The default ARIA loader source will generate a :class:`UriTextLoader` for
    locations that are URIs. For file URIs (URIs with no schemes default to file
    URIs), a base path will be extracted from the origin_location.
    """
    
    def get_loader(self, location, origin_location):
        if isinstance(location, basestring):
            # Is a string, so assume it's a URI
            paths = []
            if isinstance(origin_location, basestring):
                # Origin is a string, so assume it's a URI
                url = urlparse.urlparse(origin_location)
                if (not url.scheme) or (url.scheme == 'file'):
                    # It's a file URI, so include its base path
                    base_path = os.path.dirname(url.path)
                    paths = [base_path]
            return UriTextLoader(self, location, paths=paths)
            
        return super(DefaultLoaderSource, self).get_loader(location, origin_location)

__all__ = (
    'LoaderError',
    'LoaderNotFoundError',
    'SourceNotFoundError',
    'Loader',
    'LoaderSource',
    'LiteralLocation',
    'LiteralLoader',
    'PATHS',
    'UriLoader',
    'UriTextLoader',
    'DefaultLoaderSource')
