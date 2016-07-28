
from .templates import ServiceTemplate
from aria.presentation import Presenter
from aria.utils import ReadOnlyList

class ToscaSimplePresenter1_0(Presenter):
    """
    ARIA presenter for the `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html>`__.
    """
    
    @property
    def service_template(self):
        return ServiceTemplate(raw=self._raw)

    # Presenter

    @staticmethod
    def can_present(raw):
        dsl = raw.get('tosca_definitions_version')
        return dsl == 'tosca_simple_yaml_1_0'

    def _validate(self, context):
        self.service_template._validate(context)
    
    def _get_import_locations(self):
        return ReadOnlyList([i.file for i in self.service_template.imports] if (self.service_template and self.service_template.imports) else [])

    @property
    def repositories(self):
        return self.service_template.repositories

    @property
    def inputs(self):
        return self.service_template.topology_template.inputs
            
    @property
    def data_types(self):
        return self.service_template.data_types
    
    @property
    def node_types(self):
        return self.service_template.node_types
    
    @property
    def relationship_types(self):
        return self.service_template.relationship_types
    
    @property
    def group_types(self):
        return self.service_template.group_types

    @property
    def capability_types(self):
        return self.service_template.capability_types

    @property
    def interface_types(self):
        return self.service_template.interface_types

    @property
    def artifact_types(self):
        return self.service_template.artifact_types

    @property
    def policy_types(self):
        return self.service_template.policy_types

    @property
    def node_templates(self):
        return self.service_template.topology_template.node_templates

    @property
    def relationship_templates(self):
        return self.service_template.topology_template.relationship_templates

    @property
    def groups(self):
        return self.service_template.topology_template.groups
