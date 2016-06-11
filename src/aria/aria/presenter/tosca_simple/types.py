
from aria.presenter import Presentation, has_fields, primitive_field, primitive_list_field, object_field, object_dict_field
from definitions import PropertyDefinition, AttributeDefinition, InterfaceDefinition, RequirementDefinition, CapabilityDefinition, ArtifactDefinition
from misc import ConstraintClause
from tosca import Version

@has_fields
class ArtifactType(Presentation):
    """
    An Artifact Type is a reusable entity that defines the type of one or more files that are used to define implementation or deployment artifacts that are referenced by nodes or relationships on their operations.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_ARTIFACT_TYPE>`__
    """

    @primitive_field
    def derived_from(self):
        pass

    @object_field(Version)
    def version(self):
        """
        :class:`Version`
        """

    @primitive_field
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @primitive_field
    def mime_type(self):
        pass

    @primitive_list_field
    def file_ext(self):
        pass

    @object_dict_field(PropertyDefinition)
    def properties(self):
        """
        :class:`PropertyDefinition`
        """

@has_fields
class DataType(Presentation):
    """
    A Data Type definition defines the schema for new named datatypes in TOSCA.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_DATA_TYPE>`__
    """

    @primitive_field
    def derived_from(self):
        pass

    @object_field(Version)
    def version(self):
        """
        :class:`Version`
        """

    @primitive_field
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @object_dict_field(ConstraintClause)
    def constraints(self):
        """
        :class:`ConstraintClause`
        """

    @object_dict_field(PropertyDefinition)
    def properties(self):
        """
        :class:`PropertyDefinition`
        """

@has_fields
class CapabilityType(Presentation):
    """
    A Capability Type is a reusable entity that describes a kind of capability that a Node Type can declare to expose. Requirements (implicit or explicit) that are declared as part of one node can be matched to (i.e., fulfilled by) the Capabilities declared by another node.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_CAPABILITY_TYPE>`__
    """

    @primitive_field
    def derived_from(self):
        pass

    @object_field(Version)
    def version(self):
        """
        :class:`Version`
        """

    @primitive_field
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @object_dict_field(PropertyDefinition)
    def properties(self):
        """
        :class:`PropertyDefinition`
        """

    @object_dict_field(AttributeDefinition)
    def attributes(self):
        """
        :class:`AttributeDefinition`
        """

    @primitive_list_field
    def valid_source_types(self):
        pass

@has_fields
class InterfaceType(Presentation):
    """
    An Interface Type is a reusable entity that describes a set of operations that can be used to interact with or manage a node or relationship in a TOSCA topology.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_INTERFACE_TYPE>`__
    """

    @primitive_field
    def derived_from(self):
        pass

    @object_field(Version)
    def version(self):
        """
        :class:`Version`
        """

    @primitive_field
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @object_dict_field(PropertyDefinition)
    def inputs(self):
        """
        :class:`PropertyDefinition`
        """

@has_fields
class RelationshipType(Presentation):
    """
    A Relationship Type is a reusable entity that defines the type of one or more relationships between Node Types or Node Templates.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_RELATIONSHIP_TYPE>`__
    """

    @primitive_field
    def derived_from(self):
        pass

    @object_field(Version)
    def version(self):
        """
        :class:`Version`
        """

    @primitive_field
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @object_dict_field(PropertyDefinition)
    def properties(self):
        """
        :class:`PropertyDefinition`
        """

    @object_dict_field(AttributeDefinition)
    def attributes(self):
        """
        :class:`AttributeDefinition`
        """

    @object_dict_field(InterfaceDefinition)
    def interfaces(self):
        """
        :class:`InterfaceDefinition`
        """

    @primitive_list_field
    def valid_target_types(self):
        pass

@has_fields
class NodeType(Presentation):
    """
    A Node Type is a reusable entity that defines the type of one or more Node Templates. As such, a Node Type defines the structure of observable properties via a Properties Definition, the Requirements and Capabilities of the node as well as its supported interfaces.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_NODE_TYPE>`__
    """

    @primitive_field
    def derived_from(self):
        pass

    @object_field(Version)
    def version(self):
        """
        :class:`Version`
        """

    @primitive_field
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @object_dict_field(PropertyDefinition)
    def properties(self):
        """
        :class:`PropertyDefinition`
        """

    @object_dict_field(AttributeDefinition)
    def attributes(self):
        """
        :class:`AttributeDefinition`
        """

    @object_dict_field(RequirementDefinition)
    def requirements(self):
        """
        :class:`RequirementDefinition`
        """

    @object_dict_field(CapabilityDefinition)
    def capabilities(self):
        """
        :class:`CapabilityDefinition`
        """

    @object_dict_field(InterfaceDefinition)
    def interfaces(self):
        """
        :class:`InterfaceDefinition`
        """

    @object_dict_field(ArtifactDefinition)
    def artifacts(self):
        """
        :class:`ArtifactDefinition`
        """

@has_fields
class GroupType(Presentation):
    """
    A Group Type defines logical grouping types for nodes, typically for different management purposes. Groups can effectively be viewed as logical nodes that are not part of the physical deployment topology of an application, yet can have capabilities and the ability to attach policies and interfaces that can be applied (depending on the group type) to its member nodes.

    Conceptually, group definitions allow the creation of logical "membership" relationships to nodes in a service template that are not a part of the application's explicit requirement dependencies in the topology template (i.e. those required to actually get the application deployed and running). Instead, such logical membership allows for the introduction of things such as group management and uniform application of policies (i.e., requirements that are also not bound to the application itself) to the group's members.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_GROUP_TYPE>`__
    """

    @primitive_field
    def derived_from(self):
        pass

    @object_field(Version)
    def version(self):
        """
        :class:`Version`
        """

    @primitive_field
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @object_dict_field(PropertyDefinition)
    def properties(self):
        """
        :class:`PropertyDefinition`
        """

    @primitive_list_field
    def members(self):
        pass

    @property
    def interfaces(self):
        """
        :class:`InterfaceDefinition`
        """

@has_fields
class PolicyType(Presentation):
    """
    A Policy Type defines a type of requirement that affects or governs an application or service's topology at some stage of its lifecycle, but is not explicitly part of the topology itself (i.e., it does not prevent the application or service from being deployed or run if it did not exist).
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_POLICY_TYPE>`__
    """

    @primitive_field
    def derived_from(self):
        pass

    @object_field(Version)
    def version(self):
        """
        :class:`Version`
        """

    @primitive_field
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @object_dict_field(PropertyDefinition)
    def properties(self):
        """
        :class:`PropertyDefinition`
        """

    @primitive_list_field
    def targets(self):
        pass
