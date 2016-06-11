
from aria.presenter import Presentation, has_fields, raw_field, primitive_field, object_field, object_list_field, object_dict_field
from misc import Repository, Import
from types import ArtifactType, DataType, CapabilityType, InterfaceType, RelationshipType, NodeType, GroupType, PolicyType
from templates import TopologyTemplate

@has_fields
class Profile(Presentation):
    """
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc445238241>`__.
    """
    
    @primitive_field
    def tosca_definitions_version(self):
        """
        This required element provides a means to include a reference to the TOSCA Simple Profile specification within the TOSCA Definitions YAML file. It is an indicator for the version of the TOSCA grammar that should be used to parse the remainder of the document.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc379455047>`__
        """

    #@tosca_definitions_version.setter
    #def tosca_definitions_version(self, value):
    #    self.raw['tosca_definitions_version'] = value

    @raw_field
    def metadata(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc379455048>`__
        """

    @primitive_field
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
    
    #@description.setter
    #def description(self, value):
    #    self.raw['description'] = value
        
    @raw_field
    def dsl_definitions(self):
        # TODO ???
        pass
        
    @object_list_field(Repository)
    def repositories(self):
        """
        :class:`Repository`
        """

    @object_list_field(Import)
    def imports(self):
        """
        :class:`Import`
        """
        
    @object_dict_field(ArtifactType)
    def artifact_types(self):
        """
        :class:`ArtifactType`
        """
        
    @object_dict_field(DataType)
    def data_types(self):
        """
        :class:`DataType`
        """
        
    @object_dict_field(CapabilityType)
    def capability_types(self):
        """
        :class:`CapabilityType`
        """
        
    @object_dict_field(InterfaceType)
    def interface_types(self):
        """
        :class:`InterfaceType`
        """
        
    @object_dict_field(RelationshipType)
    def relationship_types(self):
        """
        :class:`RelationshipType`
        """

    @object_dict_field(NodeType)
    def node_types(self):
        """
        :class:`NodeType`
        """

    @object_dict_field(GroupType)
    def group_types(self):
        """
        :class:`GroupType`
        """

    @object_dict_field(PolicyType)
    def policy_types(self):
        """
        :class:`PolicyType`
        """

    @object_field(TopologyTemplate)
    def topology_template(self):
        """
        :class:`TopologyTemplate`
        """
