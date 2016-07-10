
from .loader import Loader
from .exceptions import LoaderError, DocumentNotFoundError
from requests import Session
from requests.exceptions import ConnectionError
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache

SESSION = None
SESSION_CACHE_PATH = '/tmp'

class UriLoader(Loader):
    """
    Base class for ARIA URI loaders.
    
    Extracts a document from a URI.
    
    Note that the "file:" schema is not supported: :class:`FileTextLoader` should
    be used instead.
    """

    def __init__(self, source, uri, headers={}):
        self.source = source
        self.location = uri
        self.headers = headers
        self.response = None
    
    def open(self):
        global SESSION
        if SESSION is None:
            SESSION = CacheControl(Session(), cache=FileCache(SESSION_CACHE_PATH))
            
        try:
            self.response = SESSION.get(self.location, headers=self.headers)
            status = self.response.status_code
            if status == 404:
                self.response = None
                raise DocumentNotFoundError('URI not found: "%s"' % self.location)
            elif status != 200:
                self.response = None
                raise LoaderError('URI request error %d: "%s"' % (status, self.location))
        except ConnectionError as e:
            raise LoaderError('URI connection error: "%s"' % self.location, cause=e)
        except Exception as e:
            raise LoaderError('URI error: "%s"' % self.location, cause=e)

class UriTextLoader(UriLoader):
    """
    ARIA URI text loader.
    """

    def load(self):
        if self.response is not None:
            try:
                return self.response.text
            except Exception as e:
                raise LoaderError('URI: %s' % self.location, cause=e)
        return None
