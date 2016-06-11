
from aria.presenter import HasRaw, has_properties, property_primitive, property_primitive_default, property_primitive_list, property_object, property_object_list, property_object_dict, required
from assignments import PropertyAssignment
from misc import ConstraintClause
from tosca import Range

@has_properties
class PropertyDefinition(HasRaw):
    """
    A property definition defines a named, typed value and related data that can be associated with an entity defined in this specification (e.g., Node Types, Relationship Types, Capability Types, etc.). Properties are used by template authors to provide input values to TOSCA entities which indicate their "desired state" when they are instantiated. The value of a property can be retrieved using the get_property function within TOSCA Service Templates.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_PROPERTY_DEFN>`__
    """
    
    @required
    @property_primitive
    def type(self):
        pass
    
    @property_primitive
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        return self._get_primitive('description')
        """

    @property_primitive_default(True)
    def required(self):
        pass

    @property_primitive
    def default(self):
        pass

    @property_primitive_default('supported')
    def status(self):
        pass

    @property_object_dict(ConstraintClause)
    def constraints(self):
        """
        :class:`ConstraintClause`
        """

    @property_primitive
    def entry_schema(self):
        pass

@has_properties
class AttributeDefinition(HasRaw):
    """
    An attribute definition defines a named, typed value that can be associated with an entity defined in this specification (e.g., a Node, Relationship or Capability Type). Specifically, it is used to expose the "actual state" of some property of a TOSCA entity after it has been deployed and instantiated (as set by the TOSCA orchestrator). Attribute values can be retrieved via the get_attribute function from the instance model and used as values to other entities within TOSCA Service Templates.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_ATTRIBUTE_DEFN>`__
    """

    @required
    @property_primitive
    def type(self):
        pass
    
    @property_primitive
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
        return self._get_primitive('description')

    @property_primitive
    def default(self):
        pass

    @property_primitive_default('supported')
    def status(self):
        pass

    @property_primitive
    def entry_schema(self):
        pass

@has_properties
class ParameterDefinition(HasRaw):
    """
    A parameter definition is essentially a TOSCA property definition; however, it also allows a value to be assigned to it (as for a TOSCA property assignment). In addition, in the case of output parameters, it can optionally inherit the data type of the value assigned to it rather than have an explicit data type defined for it.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_PARAMETER_DEF>`__
    """

    @property_primitive
    def type(self):
        pass

    @property_primitive
    def value(self):
        pass

@has_properties
class InterfaceDefinition(HasRaw):
    """
    An interface definition defines a named interface that can be associated with a Node or Relationship Type.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_INTERFACE_DEF>`__
    """

    @property_object_dict(ParameterDefinition)
    def inputs(self):
        """
        :class:`ParameterDefinition`
        """

    @property_object_dict(PropertyDefinition)
    def properties(self):
        """
        :class:`PropertyDefinition` or :class:`PropertyAssignment`
        """
        # TODO

@has_properties
class RequirementDefinition(HasRaw):
    """
    The Requirement definition describes a named requirement (dependencies) of a TOSCA Node Type or Node template which needs to be fulfilled by a matching Capability definition declared by another TOSCA modelable entity. The requirement definition may itself include the specific name of the fulfilling entity (explicitly) or provide an abstract type, along with additional filtering characteristics, that a TOSCA orchestrator can use to fulfill the capability at runtime (implicitly).
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_REQUIREMENT_DEF>`__
    """
    
    @required
    @property_primitive
    def capability(self):
        pass

    @property_primitive
    def node(self):
        pass

    @property_primitive
    def relationship(self):
        pass

    @property_object(Range)
    def occurrences(self):
        # TODO: range of integer
        pass

@has_properties
class CapabilityDefinition(HasRaw):
    """
    A capability definition defines a named, typed set of data that can be associated with Node Type or Node Template to describe a transparent capability or feature of the software component the node describes.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_CAPABILITY_DEFN>`__
    """
    
    @required
    @property_primitive
    def type(self):
        pass
    
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

    @property_object(Range)
    def occurrences(self):
        # TODO: range of integer
        pass

@has_properties
class ArtifactDefinition(HasRaw):
    """
    An artifact definition defines a named, typed file that can be associated with Node Type or Node Template and used by orchestration engine to facilitate deployment and implementation of interface operations.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_ARTIFACT_DEF>`__
    """
    
    @required
    @property_primitive
    def type(self):
        pass

    @required
    @property_primitive
    def file(self):
        pass
    
    @property_primitive
    def repository(self):
        pass

    @property_primitive
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @property_primitive
    def deploy_path(self):
        pass

@has_properties
class GroupDefinition(HasRaw):
    """
    A group definition defines a logical grouping of node templates, typically for management purposes, but is separate from the application's topology template.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_GROUP_DEF>`__
    """

    @required
    @property_primitive
    def type(self):
        pass

    @property_primitive
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
        pass

    @property_object_dict(PropertyAssignment)
    def properties(self):
        """
        :class:`PropertyAssignment`
        """

    @property_primitive_list
    def members(self):
        pass

    @property_object_dict(InterfaceDefinition)
    def interfaces(self):
        """
        :class:`InterfaceDefinition`
        """

@has_properties
class PolicyDefinition(HasRaw):
    """
    A policy definition defines a policy that can be associated with a TOSCA topology or top-level entity definition (e.g., group definition, node template, etc.).
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_POLICY_DEF>`__
    """

    @required
    @property_primitive
    def type(self):
        pass

    @property_primitive
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @property_object_dict(PropertyAssignment)
    def properties(self):
        """
        :class:`PropertyAssignment`
        """

    @property_primitive_list
    def targets(self):
        pass
