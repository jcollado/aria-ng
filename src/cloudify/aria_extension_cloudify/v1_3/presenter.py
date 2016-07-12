
from .templates import ServiceTemplate
from .deployment_plan import CloudifyDeploymentPlan
from aria.presentation import Presenter

class CloudifyPresenter1_3(Presenter):
    """
    ARIA presenter for the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/overview/>`__.
    """

    @property
    def service_template(self):
        return ServiceTemplate(raw=self._raw)

    # Presenter

    @staticmethod
    def can_present(raw):
        dsl = raw.get('tosca_definitions_version')
        return dsl == 'cloudify_dsl_1_3' or dsl == 'cloudify_dsl_1_2' or dsl == 'cloudify_dsl_1_1' or dsl == 'cloudify_dsl_1_0'

    def _get_import_locations(self):
        return self.service_template.imports if (self.service_template and self.service_template.imports) else []

    @property
    def deployment_plan(self):
        return CloudifyDeploymentPlan(self)

    @property
    def inputs(self):
        return self.service_template.inputs
            
    @property
    def outputs(self):
        return self.service_template.outputs

    @property
    def data_types(self):
        return self.service_template.data_types
    
    @property
    def node_types(self):
        return self.service_template.node_types
    
    @property
    def relationship_types(self):
        return self.service_template.relationships
    
    @property
    def group_types(self):
        return None
    
    @property
    def node_templates(self):
        return self.service_template.node_templates

    @property
    def relationship_templates(self):
        return None

    @property
    def groups(self):
        return self.service_template.groups

    @property
    def workflows(self):
        return self.service_template.workflows
