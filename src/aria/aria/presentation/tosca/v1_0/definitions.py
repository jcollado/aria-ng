
from .... import dsl_specification, has_fields, primitive_field, primitive_list_field, object_field, object_dict_field, field_type, field_default, required_field
from ... import Presentation
from .assignments import PropertyAssignment
from .misc import ConstraintClause
from tosca import Range

@has_fields
@dsl_specification('3.5.8', 'tosca-simple-profile-1.0')
class PropertyDefinition(Presentation):
    """
    A property definition defines a named, typed value and related data that can be associated with an entity defined in this specification (e.g., Node Types, Relationship Types, Capability Types, etc.). Properties are used by template authors to provide input values to TOSCA entities which indicate their "desired state" when they are instantiated. The value of a property can be retrieved using the get_property function within TOSCA Service Templates.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_PROPERTY_DEFN>`__
    """
    
    #@required_field # TODO: cloudify ignores this
    @field_type(str)
    @primitive_field
    def type(self):
        """
        The required data type for the property.
        
        :rtype: str
        """
    
    @field_type(str)
    @primitive_field
    def description(self):
        """
        The optional description for the property.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

    @field_default(True)
    @field_type(bool)
    @primitive_field
    def required(self):
        """
        An optional key that declares a property as required (true) or not (false).
        
        :rtype: bool
        """

    @primitive_field
    def default(self):
        """
        An optional key that may provide a value to be used as a default if not provided by another means.
        
        :rtype: str
        """

    @field_default('supported')
    @field_type(str)
    @primitive_field
    def status(self):
        """
        The optional status of the property relative to the specification or implementation.
        
        :rtype: str
        """

    @object_dict_field(ConstraintClause)
    def constraints(self):
        """
        The optional list of sequenced constraint clauses for the property.
        
        :rtype: dict of str, :class:`ConstraintClause`
        """

    @field_type(str)
    @primitive_field
    def entry_schema(self):
        """
        The optional key that is used to declare the name of the Datatype definition for entries of set types such as the TOSCA list or map.
        
        :rtype: str
        """

@has_fields
@dsl_specification('3.5.10', 'tosca-simple-profile-1.0')
class AttributeDefinition(Presentation):
    """
    An attribute definition defines a named, typed value that can be associated with an entity defined in this specification (e.g., a Node, Relationship or Capability Type). Specifically, it is used to expose the "actual state" of some property of a TOSCA entity after it has been deployed and instantiated (as set by the TOSCA orchestrator). Attribute values can be retrieved via the get_attribute function from the instance model and used as values to other entities within TOSCA Service Templates.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_ATTRIBUTE_DEFN>`__
    """

    @required_field
    @field_type(str)
    @primitive_field
    def type(self):
        """
        The required data type for the attribute.
        
        :rtype: str
        """
    
    @field_type(str)
    @primitive_field
    def description(self):
        """
        The optional description for the attribute.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """
        return self._get_primitive('description')

    @field_type(str)
    @primitive_field
    def default(self):
        """
        An optional key that may provide a value to be used as a default if not provided by another means.

        This value SHALL be type compatible with the type declared by the property definition's type keyname.
        
        :rtype: str
        """

    @field_default('supported')
    @field_type(str)
    @primitive_field
    def status(self):
        """
        The optional status of the attribute relative to the specification or implementation.
        
        :rtype: str
        """

    @field_type(str)
    @primitive_field
    def entry_schema(self):
        """
        The optional key that is used to declare the name of the Datatype definition for entries of set types such as the TOSCA list or map.
        
        :rtype: str
        """

@has_fields
@dsl_specification('3.5.12', 'tosca-simple-profile-1.0')
class ParameterDefinition(Presentation):
    """
    A parameter definition is essentially a TOSCA property definition; however, it also allows a value to be assigned to it (as for a TOSCA property assignment). In addition, in the case of output parameters, it can optionally inherit the data type of the value assigned to it rather than have an explicit data type defined for it.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_PARAMETER_DEF>`__
    """

    @field_type(str)
    @primitive_field
    def type(self):
        """
        The required data type for the parameter.

        Note: This keyname is required for a TOSCA Property definition, but is not for a TOSCA Parameter definition.
        
        :rtype: str
        """

    @primitive_field
    def value(self):
        """
        The type-compatible value to assign to the named parameter. Parameter values may be provided as the result from the evaluation of an expression or a function.
        """

@has_fields
@dsl_specification('3.5.14', 'tosca-simple-profile-1.0')
class InterfaceDefinition(Presentation):
    """
    An interface definition defines a named interface that can be associated with a Node or Relationship Type.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_INTERFACE_DEF>`__
    """

    @object_dict_field(ParameterDefinition)
    def inputs(self):
        """
        The optional list of input property definitions available to all defined operations for interface definitions that are within TOSCA Node or Relationship Type definitions. This includes when interface definitions are included as part of a Requirement definition in a Node Type.
        
        :rtype: dict of str, :class:`ParameterDefinition`
        """

    @object_dict_field(PropertyDefinition)
    def properties(self):
        """
        The optional list of input property assignments (i.e., parameters assignments) for interface definitions that are within TOSCA Node or Relationship Template definitions. This includes when interface definitions are referenced as part of a Requirement assignment in a Node Template.
        
        :rtype: dict of str, :class:`PropertyDefinition` or :class:`PropertyAssignment`
        """

@has_fields
@dsl_specification('3.6.2', 'tosca-simple-profile-1.0')
class RequirementDefinition(Presentation):
    """
    The Requirement definition describes a named requirement (dependencies) of a TOSCA Node Type or Node template which needs to be fulfilled by a matching Capability definition declared by another TOSCA modelable entity. The requirement definition may itself include the specific name of the fulfilling entity (explicitly) or provide an abstract type, along with additional filtering characteristics, that a TOSCA orchestrator can use to fulfill the capability at runtime (implicitly).
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_REQUIREMENT_DEF>`__
    """
    
    @required_field
    @field_type(str)
    @primitive_field
    def capability(self):
        """
        The required reserved keyname used that can be used to provide the name of a valid Capability Type that can fulfill the requirement.
        
        :rtype: str
        """

    @field_type(str)
    @primitive_field
    def node(self):
        """
        The optional reserved keyname used to provide the name of a valid Node Type that contains the capability definition that can be used to fulfill the requirement.
        
        :rtype: str
        """

    @field_type(str)
    @primitive_field
    def relationship(self):
        """
        The optional reserved keyname used to provide the name of a valid Relationship Type to construct when fulfilling the requirement.
        
        :rtype: str
        """

    @object_field(Range)
    def occurrences(self):
        """ 	
        The optional minimum and maximum occurrences for the requirement.

        Note: the keyword UNBOUNDED is also supported to represent any positive integer.
        
        :rtype: :class:`tosca.Range`
        """

@has_fields
@dsl_specification('3.6.1', 'tosca-simple-profile-1.0')
class CapabilityDefinition(Presentation):
    """
    A capability definition defines a named, typed set of data that can be associated with Node Type or Node Template to describe a transparent capability or feature of the software component the node describes.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_CAPABILITY_DEFN>`__
    """
    
    @required_field
    @field_type(str)
    @primitive_field
    def type(self):
        """
        The required name of the Capability Type the capability definition is based upon.
        
        :rtype: str
        """
    
    @field_type(str)
    @primitive_field
    def description(self):
        """
        The optional description of the Capability definition.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

    @object_dict_field(PropertyDefinition)
    def properties(self):
        """
        An optional list of property definitions for the Capability definition.
        
        :rtype: dict of str, :class:`PropertyDefinition`
        """

    @object_dict_field(AttributeDefinition)
    def attributes(self):
        """
        An optional list of attribute definitions for the Capability definition.
        
        :rtype: dict of str, :class:`AttributeDefinition`
        """

    @field_type(str)
    @primitive_list_field
    def valid_source_types(self):
        """
        An optional list of one or more valid names of Node Types that are supported as valid sources of any relationship established to the declared Capability Type.
        
        :rtype: list of str
        """

    @object_field(Range)
    def occurrences(self):
        """
        The optional minimum and maximum occurrences for the capability. By default, an exported Capability should allow at least one relationship to be formed with it with a maximum of UNBOUNDED relationships.

        Note: the keyword UNBOUNDED is also supported to represent any positive integer.
        
        :rtype: :class:`tosca.Range`
        """
        # TODO: range of integer

@has_fields
@dsl_specification('3.5.6', 'tosca-simple-profile-1.0')
class ArtifactDefinition(Presentation):
    """
    An artifact definition defines a named, typed file that can be associated with Node Type or Node Template and used by orchestration engine to facilitate deployment and implementation of interface operations.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_ARTIFACT_DEF>`__
    """
    
    @required_field
    @field_type(str)
    @primitive_field
    def type(self):
        """
        The required artifact type for the artifact definition.
        
        :rtype: str
        """

    @required_field
    @field_type(str)
    @primitive_field
    def file(self):
        """
        The required URI string (relative or absolute) which can be used to locate the artifact's file.
            
        :rtype: str
        """
    
    @field_type(str)
    @primitive_field
    def repository(self):
        """
        The optional name of the repository definition which contains the location of the external repository that contains the artifact. The artifact is expected to be referenceable by its file URI within the repository.
        
        :rtype: str
        """

    @field_type(str)
    @primitive_field
    def description(self):
        """
        The optional description for the artifact definition.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

    @field_type(str)
    @primitive_field
    def deploy_path(self):
        """
        The file path the associated file would be deployed into within the target node's container.
        
        :rtype: str
        """

@has_fields
@dsl_specification('3.7.5', 'tosca-simple-profile-1.0')
class GroupDefinition(Presentation):
    """
    A group definition defines a logical grouping of node templates, typically for management purposes, but is separate from the application's topology template.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_GROUP_DEF>`__
    """

    @required_field
    @field_type(str)
    @primitive_field
    def type(self):
        """
        The required name of the group type the group definition is based upon.
        
        :rtype: str
        """

    @field_type(str)
    @primitive_field
    def description(self):
        """
        The optional description for the group definition.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

    @object_dict_field(PropertyAssignment)
    def properties(self):
        """
        An optional list of property value assignments for the group definition.
        
        :rtype: dict of str, :class:`PropertyAssignment`
        """

    @field_type(str)
    @primitive_list_field
    def members(self):
        """
        The optional list of one or more node template names that are members of this group definition.
        
        :rtype: list of str
        """

    @object_dict_field(InterfaceDefinition)
    def interfaces(self):
        """
        An optional list of named interface definitions for the group definition.
        
        :rtype: dict of str, :class:`InterfaceDefinition`
        """

@has_fields
@dsl_specification('3.7.6', 'tosca-simple-profile-1.0')
class PolicyDefinition(Presentation):
    """
    A policy definition defines a policy that can be associated with a TOSCA topology or top-level entity definition (e.g., group definition, node template, etc.).
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_POLICY_DEF>`__
    """

    @required_field
    @field_type(str)
    @primitive_field
    def type(self):
        """
        The required name of the policy type the policy definition is based upon.
        
        :rtype: str
        """

    @field_type(str)
    @primitive_field
    def description(self):
        """
        The optional description for the policy definition.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

    @object_dict_field(PropertyAssignment)
    def properties(self):
        """
        An optional list of property value assignments for the policy definition.
        
        :rtype: dict of str, :class:`PropertyAssignment`
        """

    @primitive_list_field
    def targets(self):
        """
        An optional list of valid Node Templates or Groups the Policy can be applied to.
        
        :rtype: list of str
        """
