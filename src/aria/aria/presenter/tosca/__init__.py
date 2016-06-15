
from .. import Presenter
from .assignments import *
from .definitions import *
from .filters import *
from .templates import *
from .types import *
from .misc import *

class ToscaSimplePresenter1_0(Presenter):
    """
    ARIA presenter for the `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html>`__.
    """
    
    @staticmethod
    def can_present(raw):
        return raw.get('tosca_definitions_version') == 'tosca_simple_yaml_1_0'

    def validate(self, issues):
        self.service_template.validate(issues)
    
    @property
    def service_template(self):
        return ServiceTemplate(self.raw)

    def get_import_locators(self):
        return [i.file for i in self.service_template.imports] if (self.service_template and self.service_template.imports) else []

__all__ = (
    'PropertyAssignment',
    'RequirementAssignment',
    'CapabilityAssignment',
    'AttributeAssignment',
    'PropertyDefinition',
    'AttributeDefinition',
    'InterfaceDefinition',
    'RequirementDefinition',
    'CapabilityDefinition',
    'ArtifactDefinition',
    'ParameterDefinition',
    'GroupDefinition',
    'PolicyDefinition',
    'NodeFilter',
    'PropertyFilter',
    'TopologyTemplate',
    'NodeTemplate',
    'RelationshipTemplate',
    'ServiceTemplate',
    'ArtifactType',
    'DataType',
    'CapabilityType',
    'InterfaceType',
    'RelationshipType',
    'NodeType',
    'GroupType',
    'PolicyType',
    'Repository',
    'Import')
