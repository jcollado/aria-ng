
from base import Base

class PropertyDefinition(Base):
    """
    A property definition defines a named, typed value and related data that can be associated with an entity defined in this specification (e.g., Node Types, Relationship Types, Capability Types, etc.). Properties are used by template authors to provide input values to TOSCA entities which indicate their "desired state" when they are instantiated. The value of a property can be retrieved using the get_property function within TOSCA Service Templates.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_PROPERTY_DEFN>`__
    """
    
    REQUIRED = ['type']
    
    @property
    def type(self):
        return self._get_primitive('type')
    
    @property
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
        return self._get_primitive('description')

    @property
    def required(self):
        return self._get_primitive('required', True)

    @property
    def default(self):
        return self._get_primitive('default')

    @property
    def status(self):
        return self._get_primitive('status', 'supported')

    @property
    def constraints(self):
        """
        :class:`ConstraintClause`
        """
        return self._get_object_list('constraints', ConstraintClause)

    @property
    def entry_schema(self):
        return self._get_primitive('entry_schema')

class AttributeDefinition(Base):
    """
    An attribute definition defines a named, typed value that can be associated with an entity defined in this specification (e.g., a Node, Relationship or Capability Type). Specifically, it is used to expose the "actual state" of some property of a TOSCA entity after it has been deployed and instantiated (as set by the TOSCA orchestrator). Attribute values can be retrieved via the get_attribute function from the instance model and used as values to other entities within TOSCA Service Templates.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_ATTRIBUTE_DEFN>`__
    """
    
    REQUIRED = ['type']

    @property
    def type(self):
        return self._get_primitive('type')
    
    @property
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
        return self._get_primitive('description')

    @property
    def default(self):
        return self._get_primitive('default')

    @property
    def status(self):
        return self._get_primitive('status', 'supported')

    @property
    def entry_schema(self):
        return self._get_primitive('entry_schema')

class InterfaceDefinition(Base):
    """
    An interface definition defines a named interface that can be associated with a Node or Relationship Type.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_INTERFACE_DEF>`__
    """

    @property
    def inputs(self):
        """
        :class:`ParameterDefinition`
        """
        return self._get_object_list('inputs', ParameterDefinition)

    @property
    def properties(self):
        """
        :class:`PropertyDefinition` or :class:`PropertyAssignment`
        """
        # TODO
        return self._get_object_list('properties', PropertyDefinition)

class RequirementDefinition(Base):
    """
    The Requirement definition describes a named requirement (dependencies) of a TOSCA Node Type or Node template which needs to be fulfilled by a matching Capability definition declared by another TOSCA modelable entity. The requirement definition may itself include the specific name of the fulfilling entity (explicitly) or provide an abstract type, along with additional filtering characteristics, that a TOSCA orchestrator can use to fulfill the capability at runtime (implicitly).
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_REQUIREMENT_DEF>`__
    """
    
    REQUIRED = ['capability']

    @property
    def capability(self):
        return self._get_primitive('capability')

    @property
    def node(self):
        return self._get_primitive('node')

    @property
    def relationship(self):
        return self._get_primitive('relationship')

    @property
    def occurrences(self):
        # TODO: range of integer
        return self._get_object('occurrences', Range)

class CapabilityDefinition(Base):
    """
    A capability definition defines a named, typed set of data that can be associated with Node Type or Node Template to describe a transparent capability or feature of the software component the node describes.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_CAPABILITY_DEFN>`__
    """
    
    REQUIRED = ['type']

    @property
    def type(self):
        return self._get_primitive('type')
    
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

    @property
    def occurrences(self):
        # TODO: range of integer
        return self._get_object('occurrences', Range)

class ArtifactDefinition(Base):
    """
    An artifact definition defines a named, typed file that can be associated with Node Type or Node Template and used by orchestration engine to facilitate deployment and implementation of interface operations.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_ARTIFACT_DEF>`__
    """
    
    REQUIRED = ['type', 'file']

    @property
    def type(self):
        return self._get_primitive('type')

    @property
    def file(self):
        return self._get_primitive('file')
    
    @property
    def repository(self):
        return self._get_primitive('repository')

    @property
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
        return self._get_primitive('description')

    @property
    def deploy_path(self):
        return self._get_primitive('deploy_path')

class ParameterDefinition(Base):
    """
    A parameter definition is essentially a TOSCA property definition; however, it also allows a value to be assigned to it (as for a TOSCA property assignment). In addition, in the case of output parameters, it can optionally inherit the data type of the value assigned to it rather than have an explicit data type defined for it.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_PARAMETER_DEF>`__
    """

    @property
    def type(self):
        return self._get_primitive('type')

    @property
    def value(self):
        return self._get_primitive('value')

class GroupDefinition(Base):
    """
    A group definition defines a logical grouping of node templates, typically for management purposes, but is separate from the application's topology template.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_GROUP_DEF>`__
    """

    REQUIRED = ['type']

    @property
    def type(self):
        return self._get_primitive('type')

    @property
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
        return self._get_primitive('description')

    @property
    def properties(self):
        """
        :class:`PropertyAssignment`
        """
        return self._get_object_list('properties', PropertyAssignment)

    @property
    def members(self):
        return self._get_primitive_list('members')

    @property
    def interfaces(self):
        """
        :class:`InterfaceDefinition`
        """
        return self._get_object_list('interfaces', InterfaceDefinition)

class PolicyDefinition(Base):
    """
    A policy definition defines a policy that can be associated with a TOSCA topology or top-level entity definition (e.g., group definition, node template, etc.).
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_POLICY_DEF>`__
    """

    REQUIRED = ['type']

    @property
    def type(self):
        return self._get_primitive('type')

    @property
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
        return self._get_primitive('description')

    @property
    def properties(self):
        """
        :class:`PropertyAssignment`
        """
        return self._get_object_list('properties', PropertyAssignment)

    @property
    def targets(self):
        return self._get_primitive_list('targets')
