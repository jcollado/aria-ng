
from exceptions import *
from loader import *
from source import *
from string import *
from uri import *

import urlparse

class DefaultLoaderSource(LoaderSource):
    """
    The default ARIA loader source will generate a :class:`UriTextLoader` for
    locators that are URIs. For file URIs, a base path will be extracted from the
    origin_locator.
    """
    
    def get_loader(self, locator, origin_locator):
        if isinstance(locator, basestring):
            # Is a string, so assume it's a URI
            paths = []
            if isinstance(origin_locator, basestring):
                # Origin is a string, so assume it's a URI
                url = urlparse.urlparse(origin_locator)
                if (not url.scheme) or (url.scheme == 'file'):
                    # It's a file URI, so include its base path
                    base_path = os.path.dirname(url.path)
                    paths = [base_path]
            return UriTextLoader(locator, paths=paths)
            
        return super(DefaultLoaderSource, self).get_loader(locator, origin_locator)

__all__ = [
    'LoaderError',
    'LoaderNotFoundLoaderError',
    'SourceNotFoundLoaderError',
    'Loader',
    'LoaderSource',
    'StringLoader',
    'UriTextLoader',
    'DefaultLoaderSource']
