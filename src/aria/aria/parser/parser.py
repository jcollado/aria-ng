
from aria import UnimplementedAriaError, classname
from aria.loader import DefaultLoaderSource
from aria.reader import DefaultReaderSource
from aria.presenter import DefaultPresenterSource

class Parser(object):
    """
    Base class for ARIA parsers.
    
    Parsers generate presentations by consuming a data source via appropriate
    :class:`aria.loader.Loader`, :class:`aria.reader.Reader`, and :class:`aria.presenter.Presenter`
    instances.
    
    Note that parsing may internally trigger more than one loading/reading/presenting cycle,
    for example if the agnostic raw data has dependencies that must also be parsed.
    """
    
    def __init__(self, locator, reader=None, presenter_class=None, loader_source=DefaultLoaderSource(), reader_source=DefaultReaderSource(), presenter_source=DefaultPresenterSource()):
        self.locator = locator
        self.reader = reader
        self.presenter_class = presenter_class
        self.loader_source = loader_source
        self.reader_source = reader_source
        self.presenter_source = presenter_source

    def consume(self, locator):
        raise UnimplementedAriaError(classname(self) + '.parse')
