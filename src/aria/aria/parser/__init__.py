
from .. import LockedList, Issue, AriaError, print_exception
from ..consumer import Validator
from ..presenter import PresenterNotFoundError
from .exceptions import *
from .parser import *
from threading import Thread

class DefaultParser(Parser):
    """
    The default ARIA parser supports agnostic raw data composition for presenters
    that have `get_import_locations` and `merge_import`.
    
    To improve performance, loaders are called asynchronously on separate threads.
    """
    
    def parse(self):
        """
        :rtype: :class:`aria.presenter.Presenter`
        """
        presentation = self._parse_all(self.location, None, self.presenter_class)
        if presentation:
            presentation.link()
        return presentation
    
    def validate(self):
        """
        :rtype: :class:`aria.presenter.Presenter`, list of str
        """
        presentation = None
        issues = []
        try:
            presentation = self.parse()
            issues = Validator(presentation).validate()
        except Exception as e:
            issues = [Issue('%s: %s' % (e.__class__.__name__, e), e)]
            if not isinstance(e, AriaError):
                print_exception(e)
        return presentation, issues

    def _parse_all(self, location, origin_location, presenter_class, presentations=None):
        raw = self._parse_one(location, origin_location)
        
        if not presenter_class:
            try:
                presenter_class = self.presenter_source.get_presenter(raw)
            except PresenterNotFoundError:
                pass
        
        presentation = presenter_class(raw) if presenter_class else None
        
        # Handle imports
        if presentation and hasattr(presentation, 'get_import_locations') and hasattr(presentation, 'merge_import'):
            import_locations = presentation.get_import_locations()
            if import_locations:
                # TODO: this is a trivial multithreaded solution, but it may be good enough!
                # However, it can be improved by using a Queue with a thread pool
                
                imported_presentations = LockedList()
                # The imports inherit the parent presenter class
                import_threads = [Thread(target=self._parse_all, args=(import_location, location, presenter_class, imported_presentations))
                    for import_location in import_locations]
                for t in import_threads:
                    t.start()
                for t in import_threads:
                    t.join()
                for imported_presentation in imported_presentations:
                    presentation.merge_import(imported_presentation)
        
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

__all__ = (
    'ParserError',
    'Parser',
    'DefaultParser')
