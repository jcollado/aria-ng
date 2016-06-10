
from base import Base
from definitions import PropertyDefinition, AttributeDefinition, InterfaceDefinition, RequirementDefinition, CapabilityDefinition
from misc import ConstraintClause
from tosca import Version

class ArtifactType(Base):
    """
    An Artifact Type is a reusable entity that defines the type of one or more files that are used to define implementation or deployment artifacts that are referenced by nodes or relationships on their operations.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_ARTIFACT_TYPE>`__
    """

    @property
    def derived_from(self):
        return self._get_primitive('derived_from')

    @property
    def version(self):
        """
        :class:`Version`
        """
        return self._get_object('version', Version)

    @property
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
        return self._get_primitive('description')

    @property
    def mime_type(self):
        return self._get_primitive('mime_type')

    @property
    def file_ext(self):
        return self._get_primitive_list('file_ext')

    @property
    def properties(self):
        """
        :class:`PropertyDefinition`
        """
        return self._get_object_list('properties', PropertyDefinition)

class DataType(Base):
    """
    A Data Type definition defines the schema for new named datatypes in TOSCA.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_DATA_TYPE>`__
    """

    @property
    def derived_from(self):
        return self._get_primitive('derived_from')

    @property
    def version(self):
        """
        :class:`Version`
        """
        return self._get_object('version', Version)

    @property
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
        return self._get_primitive('description')

    @property
    def constraints(self):
        """
        :class:`ConstraintClause`
        """
        return self._get_object_list('constraints', ConstraintClause)

    @property
    def properties(self):
        """
        :class:`PropertyDefinition`
        """
        return self._get_object_list('properties', PropertyDefinition)

class CapabilityType(Base):
    """
    A Capability Type is a reusable entity that describes a kind of capability that a Node Type can declare to expose. Requirements (implicit or explicit) that are declared as part of one node can be matched to (i.e., fulfilled by) the Capabilities declared by another node.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_CAPABILITY_TYPE>`__
    """

    @property
    def derived_from(self):
        return self._get_primitive('derived_from')

    @property
    def version(self):
        """
        :class:`Version`
        """
        return self._get_object('version', Version)

    @property
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
        return self._get_primitive('description')

    @property
    def properties(self):
        """
        :class:`PropertyDefinition`
        """
        return self._get_object_list('properties', PropertyDefinition)

    @property
    def attributes(self):
        """
        :class:`AttributeDefinition`
        """
        return self._get_object_list('attributes', AttributeDefinition)

    @property
    def valid_source_types(self):
        return self._get_primitive_list('valid_source_types')

class InterfaceType(Base):
    """
    An Interface Type is a reusable entity that describes a set of operations that can be used to interact with or manage a node or relationship in a TOSCA topology.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_INTERFACE_TYPE>`__
    """

    @property
    def derived_from(self):
        return self._get_primitive('derived_from')

    @property
    def version(self):
        """
        :class:`Version`
        """
        return self._get_object('version', Version)

    @property
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
        return self._get_primitive('description')

    @property
    def inputs(self):
        """
        :class:`PropertyDefinition`
        """
        return self._get_object_list('inputs', PropertyDefinition)

class RelationshipType(Base):
    """
    A Relationship Type is a reusable entity that defines the type of one or more relationships between Node Types or Node Templates.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_RELATIONSHIP_TYPE>`__
    """

    @property
    def derived_from(self):
        return self._get_primitive('derived_from')

    @property
    def version(self):
        """
        :class:`Version`
        """
        return self._get_object('version', Version)

    @property
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
        return self._get_primitive('description')

    @property
    def properties(self):
        """
        :class:`PropertyDefinition`
        """
        return self._get_object_list('properties', PropertyDefinition)

    @property
    def attributes(self):
        """
        :class:`AttributeDefinition`
        """
        return self._get_object_list('attributes', AttributeDefinition)

    @property
    def interfaces(self):
        """
        :class:`InterfaceDefinition`
        """
        return self._get_object_list('interfaces', InterfaceDefinition)

    @property
    def valid_target_types(self):
        return self._get_primitive_list('valid_target_types')

class NodeType(Base):
    """
    A Node Type is a reusable entity that defines the type of one or more Node Templates. As such, a Node Type defines the structure of observable properties via a Properties Definition, the Requirements and Capabilities of the node as well as its supported interfaces.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_NODE_TYPE>`__
    """

    @property
    def derived_from(self):
        return self._get_primitive('derived_from')

    @property
    def version(self):
        """
        :class:`Version`
        """
        return self._get_object('version', Version)

    @property
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
        return self._get_primitive('description')

    @property
    def properties(self):
        """
        :class:`PropertyDefinition`
        """
        return self._get_object_list('properties', PropertyDefinition)

    @property
    def attributes(self):
        """
        :class:`AttributeDefinition`
        """
        return self._get_object_list('attributes', AttributeDefinition)

    @property
    def requirements(self):
        """
        :class:`RequirementDefinition`
        """
        return self._get_object_list('requirements', RequirementDefinition)

    @property
    def capabilities(self):
        """
        :class:`CapabilityDefinition`
        """
        return self._get_object_list('capabilities', CapabilityDefinition)

    @property
    def interfaces(self):
        """
        :class:`InterfaceDefinition`
        """
        return self._get_object_list('interfaces', InterfaceDefinition)

    @property
    def artifacts(self):
        """
        :class:`ArtifactDefinition`
        """
        return self._get_object_list('artifacts', ArtifactDefinition)

class GroupType(Base):
    """
    A Group Type defines logical grouping types for nodes, typically for different management purposes. Groups can effectively be viewed as logical nodes that are not part of the physical deployment topology of an application, yet can have capabilities and the ability to attach policies and interfaces that can be applied (depending on the group type) to its member nodes.

    Conceptually, group definitions allow the creation of logical "membership" relationships to nodes in a service template that are not a part of the application's explicit requirement dependencies in the topology template (i.e. those required to actually get the application deployed and running). Instead, such logical membership allows for the introduction of things such as group management and uniform application of policies (i.e., requirements that are also not bound to the application itself) to the group's members.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_GROUP_TYPE>`__
    """

    @property
    def derived_from(self):
        return self._get_primitive('derived_from')

    @property
    def version(self):
        """
        :class:`Version`
        """
        return self._get_object('version', Version)

    @property
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
        return self._get_primitive('description')

    @property
    def properties(self):
        """
        :class:`PropertyDefinition`
        """
        return self._get_object_list('properties', PropertyDefinition)

    @property
    def members(self):
        return self._get_primitive_list('members')

    @property
    def interfaces(self):
        """
        :class:`InterfaceDefinition`
        """
        return self._get_object_list('interfaces', InterfaceDefinition)

class PolicyType(Base):
    """
    A Policy Type defines a type of requirement that affects or governs an application or service's topology at some stage of its lifecycle, but is not explicitly part of the topology itself (i.e., it does not prevent the application or service from being deployed or run if it did not exist).
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_POLICY_TYPE>`__
    """

    @property
    def derived_from(self):
        return self._get_primitive('derived_from')

    @property
    def version(self):
        """
        :class:`Version`
        """
        return self._get_object('version', Version)

    @property
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
        return self._get_primitive('description')

    @property
    def properties(self):
        """
        :class:`PropertyDefinition`
        """
        return self._get_object_list('properties', PropertyDefinition)

    @property
    def targets(self):
        return self._get_primitive_list('targets')
