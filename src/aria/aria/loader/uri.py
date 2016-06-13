
from loader import Loader
from exceptions import LoaderError, SourceNotFoundError
import urllib, os.path

PATHS = []

class UriLoader(Loader):
    """
    Base class for ARIA URI loaders.
    
    Extracts data from a URI.
    
    If the URI does not have a scheme, it is assumed to be "file:".
    
    For file URIs, optionally supports a list of base paths that are
    tried in order if the file cannot be found.
    """

    def __init__(self, uri, paths=[]):
        self.uri = uri
        self.paths = PATHS + paths
        self.location = uri

    def open(self):
        try:
            self.file = urllib.urlopen(self.uri)
        except IOError as e:
            if e.errno == 2:
                # Not found, so try in paths
                for p in self.paths:
                    uri = os.path.join(p, self.uri)
                    try:
                        self.file = urllib.urlopen(uri)
                        self.uri = uri
                    except IOError as ee:
                        if ee.errno != 2:
                            raise ee
                if not hasattr(self, 'file'):
                    raise SourceNotFoundError('URI: "%s"' % self.uri, e)
            else:
                raise LoaderError('URI: "%s"' % self.uri, e)
        except Exception as e:
            raise LoaderError('URI: "%s"' % self.uri, e)

    def close(self):
        if hasattr(self, 'file'):
            try:
                self.file.close()
            except Exception as e:
                raise LoaderError('URI: "%s"' % self.uri, e)

class UriTextLoader(UriLoader):
    """
    ARIA URI text loader.
    """

    def load(self):
        try:
            return self.file.read()
        except Exception as e:
            raise LoaderError('URI: %s' % self.uri, e)
