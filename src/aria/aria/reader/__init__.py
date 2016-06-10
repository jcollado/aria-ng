
from aria import AriaError, UnimplementedAriaError, OpenClose, classname
import ruamel.yaml as yaml

class ReaderError(AriaError):
    """
    ARIA reader error.
    """

class ReaderNotFoundReaderError(ReaderError):
    """
    ARIA reader error: reader not found for source.
    """
    pass

class ReaderSource(object):
    """
    Base class for ARIA reader sources.
    
    Reader sources provide appropriate :class:`Reader` instances for locators.
    """

    def get_reader(self, locator, loader):
        raise UnimplementedAriaError(classname(self) + '.get_reader')

class DefaultReaderSource(ReaderSource):
    """
    The default ARIA reader source will generate a :class:`YamlReader` for
    locators that end in ".yaml".
    """

    def get_reader(self, locator, loader):
        if isinstance(locator, basestring) and locator.endswith('.yaml'):
            return YamlReader(loader)
        else:
            raise ReaderNotFoundReaderError(locator)

class Reader(object):
    """
    Base class for ARIA readers.
    
    Readers provide agnostic data structures by consuming :class:`aria.loader.Loader` instances.
    """
    
    def __init__(self, loader):
        self.loader = loader

    def load(self):
        with OpenClose(self.loader) as loader:
            return loader.consume()
    
    def consume(self):
        raise UnimplementedAriaError(classname(self) + '.read')

class YamlReader(Reader):
    """
    ARIA YAML reader.
    """
    
    def consume(self):
        source = self.load()
        try:
            return yaml.load(source, yaml.RoundTripLoader)
        except e:
            raise ReaderError('YAML', e)
