
from aria.presenter import Presentation, has_fields, primitive_field, primitive_list_field, object_field, object_list_field, object_dict_field, field_type, field_default, required_field
from assignments import PropertyAssignment
from misc import ConstraintClause
from tosca import Range

@has_fields
class PropertyDefinition(Presentation):
    """
    A property definition defines a named, typed value and related data that can be associated with an entity defined in this specification (e.g., Node Types, Relationship Types, Capability Types, etc.). Properties are used by template authors to provide input values to TOSCA entities which indicate their "desired state" when they are instantiated. The value of a property can be retrieved using the get_property function within TOSCA Service Templates.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_PROPERTY_DEFN>`__
    """
    
    #@required_field # TODO: cloudify ignores this
    @field_type(str)
    @primitive_field
    def type(self):
        pass
    
    @field_type(str)
    @primitive_field
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        return self._get_primitive('description')
        """

    @field_default(True)
    @field_type(bool)
    @primitive_field
    def required(self):
        pass

    @field_type(str)
    @primitive_field
    def default(self):
        pass

    @field_default('supported')
    @field_type(str)
    @primitive_field
    def status(self):
        pass

    @object_dict_field(ConstraintClause)
    def constraints(self):
        """
        :class:`ConstraintClause`
        """

    @field_type(str)
    @primitive_field
    def entry_schema(self):
        pass

@has_fields
class AttributeDefinition(Presentation):
    """
    An attribute definition defines a named, typed value that can be associated with an entity defined in this specification (e.g., a Node, Relationship or Capability Type). Specifically, it is used to expose the "actual state" of some property of a TOSCA entity after it has been deployed and instantiated (as set by the TOSCA orchestrator). Attribute values can be retrieved via the get_attribute function from the instance model and used as values to other entities within TOSCA Service Templates.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_ATTRIBUTE_DEFN>`__
    """

    @required_field
    @field_type(str)
    @primitive_field
    def type(self):
        pass
    
    @field_type(str)
    @primitive_field
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
        return self._get_primitive('description')

    @field_type(str)
    @primitive_field
    def default(self):
        pass

    @field_default('supported')
    @field_type(str)
    @primitive_field
    def status(self):
        pass

    @field_type(str)
    @primitive_field
    def entry_schema(self):
        pass

@has_fields
class ParameterDefinition(Presentation):
    """
    A parameter definition is essentially a TOSCA property definition; however, it also allows a value to be assigned to it (as for a TOSCA property assignment). In addition, in the case of output parameters, it can optionally inherit the data type of the value assigned to it rather than have an explicit data type defined for it.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_PARAMETER_DEF>`__
    """

    @field_type(str)
    @primitive_field
    def type(self):
        pass

    @primitive_field
    def value(self):
        pass

@has_fields
class InterfaceDefinition(Presentation):
    """
    An interface definition defines a named interface that can be associated with a Node or Relationship Type.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_INTERFACE_DEF>`__
    """

    @object_dict_field(ParameterDefinition)
    def inputs(self):
        """
        :class:`ParameterDefinition`
        """

    @object_dict_field(PropertyDefinition)
    def properties(self):
        """
        :class:`PropertyDefinition` or :class:`PropertyAssignment`
        """
        # TODO

@has_fields
class RequirementDefinition(Presentation):
    """
    The Requirement definition describes a named requirement (dependencies) of a TOSCA Node Type or Node template which needs to be fulfilled by a matching Capability definition declared by another TOSCA modelable entity. The requirement definition may itself include the specific name of the fulfilling entity (explicitly) or provide an abstract type, along with additional filtering characteristics, that a TOSCA orchestrator can use to fulfill the capability at runtime (implicitly).
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_REQUIREMENT_DEF>`__
    """
    
    @required_field
    @field_type(str)
    @primitive_field
    def capability(self):
        pass

    @field_type(str)
    @primitive_field
    def node(self):
        pass

    @field_type(str)
    @primitive_field
    def relationship(self):
        pass

    @object_field(Range)
    def occurrences(self):
        # TODO: range of integer
        pass

@has_fields
class CapabilityDefinition(Presentation):
    """
    A capability definition defines a named, typed set of data that can be associated with Node Type or Node Template to describe a transparent capability or feature of the software component the node describes.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_CAPABILITY_DEFN>`__
    """
    
    @required_field
    @field_type(str)
    @primitive_field
    def type(self):
        pass
    
    @field_type(str)
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
    @field_type(str)
    @primitive_list_field
    def valid_source_types(self):
        pass

    @object_field(Range)
    def occurrences(self):
        # TODO: range of integer
        pass

@has_fields
class ArtifactDefinition(Presentation):
    """
    An artifact definition defines a named, typed file that can be associated with Node Type or Node Template and used by orchestration engine to facilitate deployment and implementation of interface operations.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_ARTIFACT_DEF>`__
    """
    
    @required_field
    @field_type(str)
    @primitive_field
    def type(self):
        pass

    @required_field
    @field_type(str)
    @primitive_field
    def file(self):
        pass
    
    @field_type(str)
    @primitive_field
    def repository(self):
        pass

    @field_type(str)
    @primitive_field
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @field_type(str)
    @primitive_field
    def deploy_path(self):
        pass

@has_fields
class GroupDefinition(Presentation):
    """
    A group definition defines a logical grouping of node templates, typically for management purposes, but is separate from the application's topology template.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_GROUP_DEF>`__
    """

    @required_field
    @field_type(str)
    @primitive_field
    def type(self):
        pass

    @field_type(str)
    @primitive_field
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
        pass

    @object_dict_field(PropertyAssignment)
    def properties(self):
        """
        :class:`PropertyAssignment`
        """

    @field_type(str)
    @primitive_list_field
    def members(self):
        pass

    @object_dict_field(InterfaceDefinition)
    def interfaces(self):
        """
        :class:`InterfaceDefinition`
        """

@has_fields
class PolicyDefinition(Presentation):
    """
    A policy definition defines a policy that can be associated with a TOSCA topology or top-level entity definition (e.g., group definition, node template, etc.).
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_POLICY_DEF>`__
    """

    @required_field
    @primitive_field
    def type(self):
        pass

    @field_type(str)
    @primitive_field
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @object_dict_field(PropertyAssignment)
    def properties(self):
        """
        :class:`PropertyAssignment`
        """

    @primitive_list_field
    def targets(self):
        pass
