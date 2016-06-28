
from .loader import Loader
from .exceptions import LoaderError, SourceNotFoundError
from requests import Session
from requests.exceptions import HTTPError, ConnectionError, MissingSchema
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
import os.path

PATHS = []
SESSION = None
SESSION_CACHE = '/tmp'

class UriLoader(Loader):
    """
    Base class for ARIA URI loaders.
    
    Extracts data from a URI.
    
    If the URI does not have a scheme, it is assumed to be "file:".
    
    For file URIs, optionally supports a list of base paths that are
    tried in order if the file cannot be found.
    """

    def __init__(self, source, uri, paths=[]):
        self.source = source
        self.uri = uri
        self.paths = PATHS + paths
        self.location = uri
        self.headers = {}
        self.response = None
        self.file = None
    
    def open(self):
        global SESSION
        if SESSION is None:
            SESSION = CacheControl(Session(), cache=FileCache(SESSION_CACHE))
            
        try:
            self.response = SESSION.get(self.uri, headers=self.headers)
            if self.response.status_code == 200:
                return
            elif self.response.status_code == 404:
                # Not found, so try in paths
                for p in self.paths:
                    uri = os.path.join(p, self.uri)
                    self.response = SESSION.get(self.uri, headers=self.headers)
                    if self.response.status_code == 200:
                        self.uri = uri
                        return
                raise SourceNotFoundError('URI: "%s"' % self.uri, e)
            else:
                status = self.response.status_code
                self.response = None
                raise LoaderError('URI request error %d: "%s"' % (status, self.uri))
                
        except MissingSchema:
            try:
                self.file = open(self.uri, 'r')
            except IOError as e:
                if e.errno == 2:
                    # Not found, so try in paths
                    for p in self.paths:
                        uri = os.path.join(p, self.uri)
                        try:
                            self.file = open(uri, 'r')
                            self.uri = uri
                            return
                        except IOError as e:
                            if e.errno != 2:
                                raise LoaderError('URI I/O error: "%s"' % uri, e)
                    raise SourceNotFoundError('URI: "%s"' % self.uri, e)
                else:
                    raise LoaderError('URI I/O error: "%s"' % self.uri, e)
            except Exception as e:
                raise LoaderError('URI error: "%s"' % self.uri, e)

        except ConnectionError as e:
            raise LoaderError('URI connection error: "%s"' % self.uri, e)
        except Exception as e:
            raise LoaderError('URI error: "%s"' % self.uri, e)

    def close(self):
        if self.file is not None:
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
            if self.response is not None:
                return self.response.text
            elif self.file is not None:
                return self.file.read()
        except Exception as e:
            raise LoaderError('URI: %s' % self.uri, e)
        return None
