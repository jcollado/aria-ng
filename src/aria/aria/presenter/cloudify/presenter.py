
from ..tosca import ToscaSimplePresenter1_0
from .templates import ServiceTemplate

class CloudifyPresenter1_3(ToscaSimplePresenter1_0):
    """
    ARIA presenter for the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/overview/>`__.
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
