
from aria import AriaError, UnimplementedAriaError, classname
import urllib, urlparse, os.path

class LoaderError(AriaError):
    """
    ARIA loader error.
    """
    pass

class LoaderNotFoundLoaderError(LoaderError):
    """
    ARIA loader error: loader not found for source.
    """
    pass

class SourceNotFoundLoaderError(LoaderError):
    """
    ARIA loader error: resource not found.
    """
    pass

class LoaderSource(object):
    """
    Base class for ARIA loader sources.
    
    Loader sources provide appropriate :class:`Loader` instances for locators.
    """
    
    def get_loader(self, locator, origin_locator):
        raise UnimplementedAriaError(classname(self) + '.get_loader')

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
            return UriTextLoader(uri=locator, paths=paths)
        else:
            raise LoaderNotFoundLoaderError(locator)

class Loader(object):
    """
    Base class for ARIA loaders.
    
    Loaders extract data by consuming a data source.
    
    Though the extracted data is often textual (a string or string-like
    data structure), loaders may support any result.
    """
    
    def consume(self):
        raise UnimplementedAriaError(classname(self) + '.read')
    
    def open(self):
        pass

    def close(self):
        pass

class StringLoader(Loader):
    """
    ARIA string loader.
    
    This loader is a trivial holder for the provided string value.
    """

    def __init__(self, value):
        self.value = value
    
    def consume(self):
        return str(self.value)

class UriTextLoader(Loader):
    """
    ARIA URI text loader.
    
    Extracts text from a URI.
    
    If the URI does not have a scheme, it is assumed to be "file:".
    
    For file URIs, optionally supports a list of base paths that are
    tried in order if the file cannot be found.
    """

    def __init__(self, uri, paths=[]):
        self.uri = uri
        self.paths = paths

    def consume(self):
        try:
            return self._f.read()
        except e:
            raise LoaderError('URI: %s' % self.uri, e)

    def open(self):
        try:
            self._f = urllib.urlopen(self.uri)
        except IOError as e:
            if e.errno == 2:
                # Not found, so try in paths
                for p in self.paths:
                    uri = os.path.join(p, self.uri)
                    try:
                        self._f = urllib.urlopen(uri)
                        self.uri = uri
                    except IOError as ee:
                        if ee.errno != 2:
                            raise ee
                if not hasattr(self, '_f'):
                    raise SourceNotFoundLoaderError('URI: %s' % self.uri, e)
            else:
                raise Loaderrror('URI: %s' % self.uri, e)
        except e:
            raise Loaderrror('URI: %s' % self.uri, e)

    def close(self):
        if hasattr(self, '_f'):
            try:
                self._f.close()
            except e:
                raise Loaderrror('URI: %s' % self.uri, e)
