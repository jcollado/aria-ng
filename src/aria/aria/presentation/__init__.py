
from .exceptions import *
from .presenter import *
from .presentation import *
from .source import *
from .fields import *
from .validators import *

class DefaultPresenterSource(PresenterSource):
    """
    The default ARIA presenter source supports TOSCA Simple Profile and Cloudify DSLs.
    """
    
    def __init__(self, classes=None):
        from .tosca.v1_0 import ToscaSimplePresenter1_0
        from .cloudify.v1_3 import CloudifyPresenter1_3
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
    'DefaultPresenterSource',
    'Field',
    'has_fields',
    'primitive_field',
    'primitive_list_field',
    'object_field',
    'object_list_field',
    'object_dict_field',
    'field_type',
    'field_getter',
    'field_setter',
    'field_validator',
    'field_default',
    'required_field',
    'type_validator',
    'derived_from_validator')
