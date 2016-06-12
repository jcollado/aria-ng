
from loader import Loader
from exceptions import LoaderError, SourceNotFoundError
import urllib, os.path

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
        self.location = uri

    def load(self):
        try:
            return self._f.read()
        except Exception as e:
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
                    raise SourceNotFoundError('URI: "%s"' % self.uri, e)
            else:
                raise LoaderError('URI: "%s"' % self.uri, e)
        except Exception as e:
            raise LoaderError('URI: "%s"' % self.uri, e)

    def close(self):
        if hasattr(self, '_f'):
            try:
                self._f.close()
            except Exception as e:
                raise LoaderError('URI: "%s"' % self.uri, e)
