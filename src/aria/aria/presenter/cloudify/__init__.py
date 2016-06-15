
from ..tosca import ToscaSimplePresenter1_0
from .definitions import *
from .misc import *
from .profile import *
from .templates import *
from .types import *

class CloudifyPresenter1_3(ToscaSimplePresenter1_0):
    """
    ARIA presenter for Cloudify.
    """

    @staticmethod
    def can_present(raw):
        return raw.get('tosca_definitions_version') == 'cloudify_dsl_1_3'

    @property
    def profile(self):
        return Profile(self.raw)

__all__ = (
    'CloudifyPresenter1_3',
    'InterfaceDefinition',
    'Output',
    'Relationship',
    'Workflow',
    'Profile',
    'NodeTemplate',
    'NodeType',
    'RelationshipType')
