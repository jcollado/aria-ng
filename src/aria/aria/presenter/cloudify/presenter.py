
from ..tosca import ToscaSimplePresenter1_0
from .definitions import *
from .misc import *
from .templates import *
from .types import *

class CloudifyPresenter1_3(ToscaSimplePresenter1_0):
    """
    ARIA presenter for Cloudify.
    """

    @staticmethod
    def can_present(raw):
        dsl = raw.get('tosca_definitions_version')
        return dsl == 'cloudify_dsl_1_3' or dsl == 'cloudify_dsl_1_2' or dsl == 'cloudify_dsl_1_1'

    @property
    def service_template(self):
        return ServiceTemplate(self.raw)

    @property
    def inputs(self):
        return self.service_template.inputs
            
    @property
    def outputs(self):
        return self.service_template.outputs

    @property
    def relationship_types(self):
        return self.service_template.relationships
    
    @property
    def node_templates(self):
        return self.service_template.node_templates

    @property
    def groups(self):
        return self.service_template.groups

    @property
    def workflows(self):
        return self.service_template.workflows
