
from .exceptions import *
from .presenter import *
from .presentation import *
from .source import *

class DefaultPresenterSource(PresenterSource):
    """
    The default ARIA presenter source supports TOSCA Simple Profile v1.0 and Cloudify.
    """
    
    def __init__(self, classes=None):
        from .tosca import ToscaSimplePresenter1_0
        from .cloudify import CloudifyPresenter1_3
        import aria.presenter.cloudify
        self.classes = classes or [
            ToscaSimplePresenter1_0,
            CloudifyPresenter1_3]

    def get_presenter(self, raw):
        for cls in self.classes:
            if cls.can_present(raw):
                return cls
                
        return super(DefaultPresenterSource, self).get_presenter(raw)

MODULES = (
    'cloudify',
    'tosca')

__all__ = (
    'MODULES',
    'PresenterError',
    'PresenterNotFoundError',
    'Presenter',
    'Presentation',
    'PresenterSource',
    'DefaultPresenterSource')
