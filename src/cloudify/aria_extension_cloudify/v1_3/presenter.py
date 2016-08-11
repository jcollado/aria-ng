
from .templates import ServiceTemplate
from .utils.deployment import get_deployment_template
from aria.presentation import Presenter
from aria.utils import EMPTY_READ_ONLY_LIST, cachedmethod

class CloudifyPresenter1_3(Presenter):
    """
    ARIA presenter for the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/overview/>`__.
    """

    @property
    @cachedmethod
    def service_template(self):
        return ServiceTemplate(raw=self._raw)

    # Presentation

    def _dump(self, context):
        self.service_template._dump(context)

    def _validate(self, context):
        self.service_template._validate(context)

    # Presenter

    @staticmethod
    def can_present(raw):
        dsl = raw.get('tosca_definitions_version')
        return (dsl == 'cloudify_dsl_1_3') or (dsl == 'cloudify_dsl_1_2') or (dsl == 'cloudify_dsl_1_1`') or (dsl == 'cloudify_dsl_1_0')

    def _get_import_locations(self):
        return self.service_template.imports if (self.service_template and self.service_template.imports) else EMPTY_READ_ONLY_LIST

    @cachedmethod
    def _get_deployment_template(self, context):
        return get_deployment_template(context, self)

    @property
    @cachedmethod
    def repositories(self):
        return None

    @property
    @cachedmethod
    def inputs(self):
        return self.service_template.inputs
            
    @property
    @cachedmethod
    def outputs(self):
        return self.service_template.outputs

    @property
    @cachedmethod
    def data_types(self):
        return self.service_template.data_types
    
    @property
    @cachedmethod
    def node_types(self):
        return self.service_template.node_types
    
    @property
    @cachedmethod
    def relationship_types(self):
        return self.service_template.relationships
    
    @property
    @cachedmethod
    def group_types(self):
        return None

    @property
    @cachedmethod
    def capability_types(self):
        return None

    @property
    @cachedmethod
    def interface_types(self):
        return None

    @property
    @cachedmethod
    def artifact_types(self):
        return None

    @property
    @cachedmethod
    def policy_types(self):
        return None
    
    @property
    @cachedmethod
    def node_templates(self):
        return self.service_template.node_templates

    @property
    @cachedmethod
    def relationship_templates(self):
        return None

    @property
    @cachedmethod
    def groups(self):
        return self.service_template.groups

    @property
    @cachedmethod
    def policies(self):
        return self.service_template.policies

    @property
    @cachedmethod
    def policy_triggers(self):
        return self.service_template.policy_triggers

    @property
    @cachedmethod
    def workflows(self):
        return self.service_template.workflows
