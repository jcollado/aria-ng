
from ... import Presenter
from .templates import ServiceTemplate

class ToscaSimplePresenter1_0(Presenter):
    """
    ARIA presenter for the `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html>`__.
    """
    
    @staticmethod
    def can_present(raw):
        dsl = raw.get('tosca_definitions_version')
        return dsl == 'tosca_simple_yaml_1_0'

    def validate(self, issues):
        self.service_template.validate(issues)
    
    def get_import_locations(self):
        return [i.file for i in self.service_template.imports] if (self.service_template and self.service_template.imports) else []

    @property
    def service_template(self):
        return ServiceTemplate(self.raw)

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
    def node_templates(self):
        return self.service_template.topology_template.node_templates

    @property
    def relationship_templates(self):
        return self.service_template.topology_template.relationship_templates

    @property
    def groups(self):
        return self.service_template.topology_template.groups
