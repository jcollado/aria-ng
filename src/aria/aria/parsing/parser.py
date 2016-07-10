
from .. import MultithreadedExecutor, LockedList, Issue, AriaError, UnimplementedFunctionalityError, print_exception, classname
from ..consumption import Validator
from ..presentation import PresenterNotFoundError
from ..loading import DefaultLoaderSource
from ..reading import DefaultReaderSource
from ..presentation import DefaultPresenterSource

class Parser(object):
    """
    Base class for ARIA parsers.
    
    Parsers generate presentations by consuming a data source via appropriate
    :class:`aria.loader.Loader`, :class:`aria.reader.Reader`, and :class:`aria.presenter.Presenter`
    instances.
    
    Note that parsing may internally trigger more than one loading/reading/presentation cycle,
    for example if the agnostic raw data has dependencies that must also be parsed.
    """
    
    def __init__(self, location, reader=None, presenter_class=None, loader_source=DefaultLoaderSource(), reader_source=DefaultReaderSource(), presenter_source=DefaultPresenterSource()):
        self.location = location
        self.reader = reader
        self.presenter_class = presenter_class
        self.loader_source = loader_source
        self.reader_source = reader_source
        self.presenter_source = presenter_source

    def parse(self, location):
        raise UnimplementedFunctionalityError(classname(self) + '.parse')

class DefaultParser(Parser):
    """
    The default ARIA parser supports agnostic raw data composition for presenters
    that have `_get_import_locations` and `_merge_import`.
    
    To improve performance, loaders are called asynchronously on separate threads.
    """
    
    def parse(self):
        """
        :rtype: :class:`aria.presenter.Presenter`
        """
        presentation = self._parse_all(self.location, None, self.presenter_class)
        if presentation and hasattr(presentation, '_link'):
            presentation._link()
        return presentation
    
    def parse_and_validate(self, consumption_context):
        """
        :rtype: :class:`aria.presenter.Presenter`, list of str
        """
        try:
            consumption_context.presentation = self.parse()
            Validator(consumption_context).consume()
        except Exception as e:
            if hasattr(e, 'issue') and isinstance(e.issue, Issue):
                consumption_context.validation.issues.append(e.issue)
            else:
                consumption_context.validation.issues.append(Issue('%s' % e.__class__.__name__, cause=e))
            if not isinstance(e, AriaError):
                print_exception(e)

    def _parse_all(self, location, origin_location, presenter_class, presentations=None):
        raw = self._parse_one(location, origin_location)
        
        if not presenter_class:
            try:
                presenter_class = self.presenter_source.get_presenter(raw)
            except PresenterNotFoundError:
                pass
        
        presentation = presenter_class(raw=raw) if presenter_class else None
        
        # Handle imports
        if presentation and hasattr(presentation, '_get_import_locations') and hasattr(presentation, '_merge_import'):
            import_locations = presentation._get_import_locations()
            if import_locations:
                executor = MultithreadedExecutor()
                imported_presentations = LockedList()
                for import_location in import_locations:
                    # The imports inherit the parent presenter class
                    executor.submit(self._parse_all, (import_location, location, presenter_class, imported_presentations))
                executor.join_all()
                for imported_presentation in imported_presentations:
                    presentation._merge_import(imported_presentation)
        
        if presentation and presentations is not None:
            with presentations:
                presentations.append(presentation)
        
        return presentation
    
    def _parse_one(self, location, origin_location):
        if self.reader:
            return self.reader.read()
        loader = self.loader_source.get_loader(location, origin_location)
        reader = self.reader_source.get_reader(location, loader)
        return reader.read()
