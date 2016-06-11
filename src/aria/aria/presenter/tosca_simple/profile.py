
from aria.presenter import HasRaw, has_properties, property_raw, property_primitive, property_object, property_object_list, property_object_dict
from misc import Repository, Import
from types import ArtifactType, DataType, CapabilityType, InterfaceType, RelationshipType, NodeType, GroupType, PolicyType
from templates import TopologyTemplate

@has_properties
class Profile(HasRaw):
    """
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc445238241>`__.
    """
    
    @property_primitive
    def tosca_definitions_version(self):
        """
        This required element provides a means to include a reference to the TOSCA Simple Profile specification within the TOSCA Definitions YAML file. It is an indicator for the version of the TOSCA grammar that should be used to parse the remainder of the document.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc379455047>`__
        """

    #@tosca_definitions_version.setter
    #def tosca_definitions_version(self, value):
    #    self.raw['tosca_definitions_version'] = value

    @property_raw
    def metadata(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc379455048>`__
        """

    @property_primitive
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
    
    #@description.setter
    #def description(self, value):
    #    self.raw['description'] = value
        
    @property_raw
    def dsl_definitions(self):
        # TODO ???
        pass
        
    @property_object_list(Repository)
    def repositories(self):
        """
        :class:`Repository`
        """

    @property_object_list(Import)
    def imports(self):
        """
        :class:`Import`
        """
        
    @property_object_dict(ArtifactType)
    def artifact_types(self):
        """
        :class:`ArtifactType`
        """
        
    @property_object_dict(DataType)
    def data_types(self):
        """
        :class:`DataType`
        """
        
    @property_object_dict(CapabilityType)
    def capability_types(self):
        """
        :class:`CapabilityType`
        """
        
    @property_object_dict(InterfaceType)
    def interface_types(self):
        """
        :class:`InterfaceType`
        """
        
    @property_object_dict(RelationshipType)
    def relationship_types(self):
        """
        :class:`RelationshipType`
        """

    @property_object_dict(NodeType)
    def node_types(self):
        """
        :class:`NodeType`
        """

    @property_object_dict(GroupType)
    def group_types(self):
        """
        :class:`GroupType`
        """

    @property_object_dict(PolicyType)
    def policy_types(self):
        """
        :class:`PolicyType`
        """

    @property_object(TopologyTemplate)
    def topology_template(self):
        """
        :class:`TopologyTemplate`
        """
