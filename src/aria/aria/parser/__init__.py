
from exceptions import *
from parser import *

from aria.presenter import PresenterNotFoundError

class DefaultParser(Parser):
    """
    The default ARIA parser supports agnostic raw data composition for presenters
    that have `get_import_locators` and `merge_import`.
    """
    
    def parse(self):
        """
        :class:`aria.presenter.Presenter` or raw
        """
        presentation = self._parse_all(self.locator, None, self.presenter_class)
        if presentation:
            presentation.link()
        return presentation

    def _parse_all(self, locator, origin_locator, presenter_class):
        raw = self._parse_one(locator, origin_locator)
        
        if not presenter_class:
            try:
                presenter_class = self.presenter_source.get_presenter(raw)
            except PresenterNotFoundError:
                pass
        
        presentation = presenter_class(raw) if presenter_class else None
        
        # Handle imports
        if presentation and hasattr(presentation, 'get_import_locators') and hasattr(presentation, 'merge_import'):
            import_locators = presentation.get_import_locators()
            for import_locator in import_locators:
                # The imports inherit the parent presenter class
                imported_presentation = self._parse_all(import_locator, locator, presenter_class)
                presentation.merge_import(imported_presentation)
        
        return presentation
    
    def _parse_one(self, locator, origin_locator):
        if self.reader:
            return self.reader.read()
        loader = self.loader_source.get_loader(locator, origin_locator)
        reader = self.reader_source.get_reader(locator, loader)
        return reader.read()

__all__ = (
    'ParserError',
    'Parser',
    'DefaultParser')
