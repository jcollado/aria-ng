
from base import Base
from misc import Repository, Import
from types import ArtifactType, DataType, CapabilityType, InterfaceType, RelationshipType, NodeType, GroupType, PolicyType
from templates import TopologyTemplate

class Profile(Base):
    """
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc445238241>`__.
    """

    @property
    def tosca_definitions_version(self):
        """
        This required element provides a means to include a reference to the TOSCA Simple Profile specification within the TOSCA Definitions YAML file.  It is an indicator for the version of the TOSCA presenter that should be used to parse the remainder of the document.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc379455047>`__
        """
        return self._get_primitive('tosca_definitions_version')
        
    @tosca_definitions_version.setter
    def tosca_definitions_version(self, value):
        self.raw['tosca_definitions_version'] = value

    @property
    def metadata(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc379455048>`__
        """
        return self.raw.get('metadata')

    @property
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
        return self._get_primitive('description')
    
    @description.setter
    def description(self, value):
        self.raw['description'] = value
        
    @property
    def dsl_definitions(self):
        # TODO ???
        return self.raw.get('dsl_definitions')
        
    @property
    def repositories(self):
        """
        :class:`Repository`
        """
        return self._get_object_list('repositories', Repository)

    @property
    def imports(self):
        """
        :class:`Import`
        """
        return self._get_object_list('imports', Import)
        
    @property
    def artifact_types(self):
        """
        :class:`ArtifactType`
        """
        return self._get_object_list('artifacts', ArtifactType)
        
    @property
    def data_types(self):
        """
        :class:`DataType`
        """
        return self._get_object_list('data_types', DataType)
        
    @property
    def capability_types(self):
        """
        :class:`CapabilityType`
        """
        return self._get_object_list('capability_types', CapabilityType)
        
    @property
    def interface_types(self):
        """
        :class:`InterfaceType`
        """
        return self._get_object_list('interface_types', InterfaceType)
        
    @property
    def relationship_types(self):
        """
        :class:`RelationshipType`
        """
        return self._get_object_list('relationship_types', RelationshipType)

    @property
    def node_types(self):
        """
        :class:`NodeType`
        """
        return self._get_object_list('node_types', NodeType)

    @property
    def group_types(self):
        """
        :class:`GroupType`
        """
        return self._get_object_list('group_types', GroupType)

    @property
    def policy_types(self):
        """
        :class:`PolicyType`
        """
        return self._get_object_list('policy_types', PolicyType)

    @property
    def topology_template(self):
        """
        :class:`TopologyTemplate`
        """
        return self._get_object('topology_template', TopologyTemplate)
