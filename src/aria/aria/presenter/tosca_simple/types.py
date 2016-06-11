
from aria.presenter import HasRaw, has_properties, property_primitive, property_primitive_list, property_object, property_object_dict
from definitions import PropertyDefinition, AttributeDefinition, InterfaceDefinition, RequirementDefinition, CapabilityDefinition, ArtifactDefinition
from misc import ConstraintClause
from tosca import Version

@has_properties
class ArtifactType(HasRaw):
    """
    An Artifact Type is a reusable entity that defines the type of one or more files that are used to define implementation or deployment artifacts that are referenced by nodes or relationships on their operations.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_ARTIFACT_TYPE>`__
    """

    @property_primitive
    def derived_from(self):
        pass

    @property_object(Version)
    def version(self):
        """
        :class:`Version`
        """

    @property_primitive
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @property_primitive
    def mime_type(self):
        pass

    @property_primitive_list
    def file_ext(self):
        pass

    @property_object_dict(PropertyDefinition)
    def properties(self):
        """
        :class:`PropertyDefinition`
        """

@has_properties
class DataType(HasRaw):
    """
    A Data Type definition defines the schema for new named datatypes in TOSCA.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_DATA_TYPE>`__
    """

    @property_primitive
    def derived_from(self):
        pass

    @property_object(Version)
    def version(self):
        """
        :class:`Version`
        """

    @property_primitive
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @property_object_dict(ConstraintClause)
    def constraints(self):
        """
        :class:`ConstraintClause`
        """

    @property_object_dict(PropertyDefinition)
    def properties(self):
        """
        :class:`PropertyDefinition`
        """

@has_properties
class CapabilityType(HasRaw):
    """
    A Capability Type is a reusable entity that describes a kind of capability that a Node Type can declare to expose. Requirements (implicit or explicit) that are declared as part of one node can be matched to (i.e., fulfilled by) the Capabilities declared by another node.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_CAPABILITY_TYPE>`__
    """

    @property_primitive
    def derived_from(self):
        pass

    @property_object(Version)
    def version(self):
        """
        :class:`Version`
        """

    @property_primitive
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @property_object_dict(PropertyDefinition)
    def properties(self):
        """
        :class:`PropertyDefinition`
        """

    @property_object_dict(AttributeDefinition)
    def attributes(self):
        """
        :class:`AttributeDefinition`
        """

    @property_primitive_list
    def valid_source_types(self):
        pass

@has_properties
class InterfaceType(HasRaw):
    """
    An Interface Type is a reusable entity that describes a set of operations that can be used to interact with or manage a node or relationship in a TOSCA topology.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_INTERFACE_TYPE>`__
    """

    @property_primitive
    def derived_from(self):
        pass

    @property_object(Version)
    def version(self):
        """
        :class:`Version`
        """

    @property_primitive
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @property_object_dict(PropertyDefinition)
    def inputs(self):
        """
        :class:`PropertyDefinition`
        """

@has_properties
class RelationshipType(HasRaw):
    """
    A Relationship Type is a reusable entity that defines the type of one or more relationships between Node Types or Node Templates.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_RELATIONSHIP_TYPE>`__
    """

    @property_primitive
    def derived_from(self):
        pass

    @property_object(Version)
    def version(self):
        """
        :class:`Version`
        """

    @property_primitive
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @property_object_dict(PropertyDefinition)
    def properties(self):
        """
        :class:`PropertyDefinition`
        """

    @property_object_dict(AttributeDefinition)
    def attributes(self):
        """
        :class:`AttributeDefinition`
        """

    @property_object_dict(InterfaceDefinition)
    def interfaces(self):
        """
        :class:`InterfaceDefinition`
        """

    @property_primitive_list
    def valid_target_types(self):
        pass

@has_properties
class NodeType(HasRaw):
    """
    A Node Type is a reusable entity that defines the type of one or more Node Templates. As such, a Node Type defines the structure of observable properties via a Properties Definition, the Requirements and Capabilities of the node as well as its supported interfaces.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_NODE_TYPE>`__
    """

    @property_primitive
    def derived_from(self):
        pass

    @property_object(Version)
    def version(self):
        """
        :class:`Version`
        """

    @property_primitive
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @property_object_dict(PropertyDefinition)
    def properties(self):
        """
        :class:`PropertyDefinition`
        """

    @property_object_dict(AttributeDefinition)
    def attributes(self):
        """
        :class:`AttributeDefinition`
        """

    @property_object_dict(RequirementDefinition)
    def requirements(self):
        """
        :class:`RequirementDefinition`
        """

    @property_object_dict(CapabilityDefinition)
    def capabilities(self):
        """
        :class:`CapabilityDefinition`
        """

    @property_object_dict(InterfaceDefinition)
    def interfaces(self):
        """
        :class:`InterfaceDefinition`
        """

    @property_object_dict(ArtifactDefinition)
    def artifacts(self):
        """
        :class:`ArtifactDefinition`
        """

@has_properties
class GroupType(HasRaw):
    """
    A Group Type defines logical grouping types for nodes, typically for different management purposes. Groups can effectively be viewed as logical nodes that are not part of the physical deployment topology of an application, yet can have capabilities and the ability to attach policies and interfaces that can be applied (depending on the group type) to its member nodes.

    Conceptually, group definitions allow the creation of logical "membership" relationships to nodes in a service template that are not a part of the application's explicit requirement dependencies in the topology template (i.e. those required to actually get the application deployed and running). Instead, such logical membership allows for the introduction of things such as group management and uniform application of policies (i.e., requirements that are also not bound to the application itself) to the group's members.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_GROUP_TYPE>`__
    """

    @property_primitive
    def derived_from(self):
        pass

    @property_object(Version)
    def version(self):
        """
        :class:`Version`
        """

    @property_primitive
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @property_object_dict(PropertyDefinition)
    def properties(self):
        """
        :class:`PropertyDefinition`
        """

    @property_primitive_list
    def members(self):
        pass

    @property
    def interfaces(self):
        """
        :class:`InterfaceDefinition`
        """

@has_properties
class PolicyType(HasRaw):
    """
    A Policy Type defines a type of requirement that affects or governs an application or service's topology at some stage of its lifecycle, but is not explicitly part of the topology itself (i.e., it does not prevent the application or service from being deployed or run if it did not exist).
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_POLICY_TYPE>`__
    """

    @property_primitive
    def derived_from(self):
        pass

    @property_object(Version)
    def version(self):
        """
        :class:`Version`
        """

    @property_primitive
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @property_object_dict(PropertyDefinition)
    def properties(self):
        """
        :class:`PropertyDefinition`
        """

    @property_primitive_list
    def targets(self):
        pass
