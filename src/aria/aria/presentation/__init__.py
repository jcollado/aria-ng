
from .exceptions import *
from .presenter import *
from .presentation import *
from .source import *
from .fields import *
from .validators import *

PRESENTER_CLASSES = []

class DefaultPresenterSource(PresenterSource):
    """
    The default ARIA presenter source supports TOSCA Simple Profile and Cloudify DSLs.
    """
    
    def __init__(self, classes=PRESENTER_CLASSES):
        self.classes = classes
        #from tosca_dsl.v1_0 import ToscaSimplePresenter1_0
        #from cloudify_dsl.v1_3 import CloudifyPresenter1_3
        #self.classes = classes or [
        #    ToscaSimplePresenter1_0,
        #    CloudifyPresenter1_3]

    def get_presenter(self, raw):
        for cls in self.classes:
            if cls.can_present(raw):
                return cls
                
        return super(DefaultPresenterSource, self).get_presenter(raw)

__all__ = (
    'MODULES',
    'PresenterError',
    'PresenterNotFoundError',
    'Presenter',
    'Presentation',
    'PresenterSource',
    'PRESENTER_CLASSES'
    'DefaultPresenterSource',
    'Field',
    'has_fields',
    'short_form_field',
    'primitive_field',
    'primitive_list_field',
    'object_field',
    'object_list_field',
    'object_dict_field',
    'field_getter',
    'field_setter',
    'field_validator',
    'type_validator',
    'derived_from_validator')
