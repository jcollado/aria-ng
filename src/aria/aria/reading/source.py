
from ..loading import LiteralLocation
from .exceptions import ReaderNotFoundError
from .yaml import YamlReader
from .jinja import JinjaReader

class ReaderSource(object):
    """
    Base class for ARIA reader sources.
    
    Reader sources provide appropriate :class:`Reader` instances for locations.
    """

    def get_reader(self, location, loader):
        raise ReaderNotFoundError('location: %s' % location)

EXTENSIONS = {
    '.yaml': YamlReader,
    '.jinja': JinjaReader}

class DefaultReaderSource(ReaderSource):
    """
    The default ARIA reader source will generate a :class:`YamlReader` for
    locations that end in ".yaml", and a :class:`JinjaReader` for locations
    that end in ".jinja". 
    """
    
    def __init__(self, literal_reader_class=YamlReader):
        super(DefaultReaderSource, self).__init__()
        self.literal_reader_class = literal_reader_class

    def get_reader(self, location, loader):
        if isinstance(location, LiteralLocation):
            return self.literal_reader_class(self, location, loader)
        elif isinstance(location, basestring):
            for extension, reader_class in EXTENSIONS.iteritems():
                if location.endswith(extension):
                    return reader_class(self, location, loader)
        return super(DefaultReaderSource, self).get_reader(location, loader)
