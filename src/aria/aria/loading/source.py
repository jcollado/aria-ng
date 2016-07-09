
from .exceptions import LoaderNotFoundError
from .literal import LiteralLocation, LiteralLoader
from .file import FileTextLoader
from .uri import UriTextLoader
import urlparse, os.path

class LoaderSource(object):
    """
    Base class for ARIA loader sources.
    
    Loader sources provide appropriate :class:`Loader` instances for locations.
    
    A :class:`LiteralLocation` is handled specially by wrapping the literal value
    in a :class:`LiteralLoader`.
    """
    
    def get_loader(self, location, origin_location):
        if isinstance(location, LiteralLocation):
            return LiteralLoader(location.value)
        raise LoaderNotFoundError(location)

class DefaultLoaderSource(LoaderSource):
    """
    The default ARIA loader source will generate a :class:`UriTextLoader` for
    locations that are non-file URIs, and a :class:`FileTextLoader` for file
    URIs and other strings.
    
    If :class:`FileTextLoader` is used, a base path will be extracted from
    origin_location.
    """
    
    def get_loader(self, location, origin_location):
        if isinstance(location, basestring):
            url = urlparse.urlparse(location)
            if (not url.scheme) or (url.scheme == 'file'):
                # It's a file
                if url.scheme == 'file':
                    location = url.path
                paths = []

                # Check origin_location
                if isinstance(origin_location, basestring):
                    url = urlparse.urlparse(origin_location)
                    if (not url.scheme) or (url.scheme == 'file'):
                        # It's a file, so include its base path
                        base_path = os.path.dirname(url.path)
                        paths = [base_path]
                
                return FileTextLoader(self, location, paths=paths)
            else:
                # It's a URL
                return UriTextLoader(self, location)
            
        return super(DefaultLoaderSource, self).get_loader(location, origin_location)
