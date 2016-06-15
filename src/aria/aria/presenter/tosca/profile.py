
from ... import tosca_specification, has_fields, primitive_field, object_field, object_list_field, object_dict_field, field_type, required_field
from .. import Presentation
from .misc import Repository, Import
from .types import ArtifactType, DataType, CapabilityType, InterfaceType, RelationshipType, NodeType, GroupType, PolicyType
from .templates import TopologyTemplate

@has_fields
@tosca_specification('3')
class Profile(Presentation):
    """
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc445238241>`__.
    """
    
    @field_type(str)
    @primitive_field
    def tosca_definitions_version():
        """
        Defines the version of the TOSCA Simple Profile specification the template (grammar) complies with. 
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc379455047>`__
        
        :rtype: str
        """

    @primitive_field
    def metadata():
        """
        Defines a section used to declare additional metadata information.  Domain-specific TOSCA profile specifications may define keynames that are required for their implementations.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc379455048>`__
        """

    @field_type(str)
    @required_field # test
    @primitive_field
    def description():
        """
        Declares a description for this Service Template and its contents.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """
    
    @primitive_field
    def dsl_definitions():
        """
        Declares optional DSL-specific definitions and conventions.  For example, in YAML, this allows defining reusable YAML macros (i.e., YAML alias anchors) for use throughout the TOSCA Service Template.
        """
        
    @object_list_field(Repository)
    def repositories():
        """
        Declares the list of external repositories which contain artifacts that are referenced in the service template along with their addresses and necessary credential information used to connect to them in order to retrieve the artifacts.
        
        :rtype: list of :class:`Repository`
        """

    @object_list_field(Import)
    def imports():
        """
        Declares import statements external TOSCA Definitions documents. For example, these may be file location or URIs relative to the service template file within the same TOSCA CSAR file.
        
        :rtype: list of :class:`Import`
        """
        
    @object_dict_field(ArtifactType)
    def artifact_types():
        """
        This section contains an optional list of artifact type definitions for use in the service template.
        
        :rtype: dict of str, :class:`ArtifactType`
        """
        
    @object_dict_field(DataType)
    def data_types():
        """
        Declares a list of optional TOSCA Data Type definitions.
        
        :rtype: dict of str, :class:`DataType`
        """
        
    @object_dict_field(CapabilityType)
    def capability_types():
        """
        This section contains an optional list of capability type definitions for use in the service template.
        
        :rtype: dict of str, :class:`CapabilityType`
        """
        
    @object_dict_field(InterfaceType)
    def interface_types():
        """
        This section contains an optional list of interface type definitions for use in the service template.
        
        :rtype: dict of str, :class:`InterfaceType`
        """
        
    @object_dict_field(RelationshipType)
    def relationship_types():
        """
        This section contains a set of relationship type definitions for use in the service template.
        
        :rtype: dict of str, :class:`RelationshipType`
        """

    @object_dict_field(NodeType)
    def node_types():
        """
        This section contains a set of node type definitions for use in the service template.
        
        :rtype: dict of str, :class:`NodeType`
        """

    @object_dict_field(GroupType)
    def group_types():
        """
        This section contains a list of group type definitions for use in the service template.
        
        :rtype: dict of str, :class:`GroupType`
        """

    @object_dict_field(PolicyType)
    def policy_types():
        """
        This section contains a list of policy type definitions for use in the service template.
        
        :rtype: dict of str, :class:`PolicyType`
        """

    @object_field(TopologyTemplate)
    def topology_template():
        """
        Defines the topology template of an application or service, consisting of node templates that represent the application's or service's components, as well as relationship templates representing relations between the components.
        
        :rtype: :class:`TopologyTemplate`
        """
