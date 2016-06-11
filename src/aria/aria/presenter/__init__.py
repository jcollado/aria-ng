
from exceptions import *
from utils import *
from presenter import *
from source import *

class DefaultPresenterSource(PresenterSource):
    """
    The default ARIA presenter source supports TOSCA Simple Profile v1.0 and Cloudify.
    """
    
    def __init__(self, classes=None):
        import aria.presenter.tosca_simple
        import aria.presenter.cloudify
        self.classes = classes or [
            aria.presenter.tosca_simple.ToscaSimplePresenter1_0,
            aria.presenter.cloudify.CloudifyPresenter1_3]

    def get_presenter(self, raw):
        for cls in self.classes:
            if cls.can_present(raw):
                return cls
                
        return super(DefaultPresenterSource, self).get_presenter(raw)

__all__ = [
    'PresenterError',
    'PresenterNotFoundPresenterError',
    'Presentation',
    'has_fields',
    'raw_field',
    'primitive_field',
    'primitive_field_with_default',
    'primitive_list_field',
    'object_field',
    'object_list_field',
    'object_dict_field',
    'required_field',
    'Presenter',
    'PresenterSource',
    'DefaultPresenterSource']
