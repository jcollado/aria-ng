
from .presentation import ToscaPresentation
from .misc import Description, PropertyAssignment, ConstraintClause
from .data_types import Range
from .field_getters import data_type_class_getter
from .field_validators import data_type_validator, data_value_validator, entry_schema_validator, policy_node_template_or_group_validator
from .utils.data_types import get_data_type, get_property_constraints
from .utils.properties import get_assigned_and_defined_property_values
from .utils.interfaces import get_and_override_input_definitions_from_type, get_and_override_operation_definitions_from_type, get_template_interfaces
from .utils.policies import get_policy_targets
from aria import dsl_specification
from aria.utils import ReadOnlyList, ReadOnlyDict, cachedmethod
from aria.presentation import has_fields, short_form_field, allow_unknown_fields, primitive_field, primitive_list_field, object_field, object_list_field, object_dict_field, object_dict_unknown_fields, field_validator, field_getter, type_validator, list_type_validator

@short_form_field('type')
@has_fields
class EntrySchema(ToscaPresentation):
    """
    The specification does not properly explain this type, however it is implied by examples.
    """
    
    @field_validator(data_type_validator('entry schema data type'))
    @primitive_field(str, required=True)
    def type(self):
        """
        :rtype: str
        """

    @object_field(Description)
    def description(self):
        """
        :rtype: :class:`Description`
        """

    @object_list_field(ConstraintClause)
    def constraints(self):
        """
        :rtype: list of (str, :class:`ConstraintClause`)
        """

    @cachedmethod
    def _get_type(self, context):
        return get_data_type(context, self, 'type')

    @cachedmethod
    def _get_constraints(self, context):
        return get_property_constraints(context, self)

@has_fields
@dsl_specification('3.5.8', 'tosca-simple-profile-1.0')
class PropertyDefinition(ToscaPresentation):
    """
    A property definition defines a named, typed value and related data that can be associated with an entity defined in this specification (e.g., Node Types, Relationship Types, Capability Types, etc.). Properties are used by template authors to provide input values to TOSCA entities which indicate their "desired state" when they are instantiated. The value of a property can be retrieved using the get_property function within TOSCA Service Templates.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_PROPERTY_DEFN>`__
    """
    
    @field_validator(data_type_validator())
    @primitive_field(str, required=True)
    def type(self):
        """
        The required data type for the property.
        
        :rtype: str
        """
    
    @object_field(Description)
    def description(self):
        """
        The optional description for the property.
        
        :rtype: :class:`Description`
        """

    @primitive_field(bool, default=True)
    def required(self):
        """
        An optional key that declares a property as required (true) or not (false).
        
        :rtype: bool
        """

    @field_validator(data_value_validator)
    @primitive_field()
    def default(self):
        """
        An optional key that may provide a value to be used as a default if not provided by another means.
        
        :rtype: str
        """

    @primitive_field(str, default='supported', allowed=('supported', 'unsupported', 'experimental', 'deprecated'))
    @dsl_specification(section='3.5.8.3', spec='tosca-simple-profile-1.0')
    def status(self):
        """
        The optional status of the property relative to the specification or implementation.
        
        :rtype: str
        """

    @object_list_field(ConstraintClause)
    def constraints(self):
        """
        The optional list of sequenced constraint clauses for the property.
        
        :rtype: list of (str, :class:`ConstraintClause`)
        """

    @field_validator(entry_schema_validator)
    @object_field(EntrySchema)
    def entry_schema(self):
        """
        The optional key that is used to declare the name of the Datatype definition for entries of set types such as the TOSCA list or map.
        
        :rtype: str
        """
    
    @cachedmethod
    def _get_type(self, context):
        return get_data_type(context, self, 'type')

    @cachedmethod
    def _get_constraints(self, context):
        return get_property_constraints(context, self)

@has_fields
@dsl_specification('3.5.10', 'tosca-simple-profile-1.0')
class AttributeDefinition(ToscaPresentation):
    """
    An attribute definition defines a named, typed value that can be associated with an entity defined in this specification (e.g., a Node, Relationship or Capability Type). Specifically, it is used to expose the "actual state" of some property of a TOSCA entity after it has been deployed and instantiated (as set by the TOSCA orchestrator). Attribute values can be retrieved via the get_attribute function from the instance model and used as values to other entities within TOSCA Service Templates.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_ATTRIBUTE_DEFN>`__
    """

    @field_validator(data_type_validator())
    @primitive_field(str, required=True)
    def type(self):
        """
        The required data type for the attribute.
        
        :rtype: str
        """
    
    @object_field(Description)
    def description(self):
        """
        The optional description for the attribute.
        
        :rtype: :class:`Description`
        """

    @field_validator(data_value_validator)
    @primitive_field(str)
    def default(self):
        """
        An optional key that may provide a value to be used as a default if not provided by another means.

        This value SHALL be type compatible with the type declared by the property definition's type keyname.
        
        :rtype: str
        """

    @primitive_field(str, default='supported', allowed=('supported', 'unsupported', 'experimental', 'deprecated'))
    def status(self):
        """
        The optional status of the attribute relative to the specification or implementation.
        
        :rtype: str
        """

    @field_validator(entry_schema_validator)
    @object_field(EntrySchema)
    def entry_schema(self):
        """
        The optional key that is used to declare the name of the Datatype definition for entries of set types such as the TOSCA list or map.
        
        :rtype: str
        """

    @cachedmethod
    def _get_type(self, context):
        return get_data_type(context, self, 'type')

@has_fields
@dsl_specification('3.5.12', 'tosca-simple-profile-1.0')
class ParameterDefinition(PropertyDefinition):
    """
    A parameter definition is essentially a TOSCA property definition; however, it also allows a value to be assigned to it (as for a TOSCA property assignment). In addition, in the case of output parameters, it can optionally inherit the data type of the value assigned to it rather than have an explicit data type defined for it.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_PARAMETER_DEF>`__
    """

    @field_validator(data_type_validator())
    @primitive_field(str)
    def type(self):
        """
        The required data type for the parameter.

        Note: This keyname is required for a TOSCA Property definition, but is not for a TOSCA Parameter definition.
        
        :rtype: str
        """

    @field_validator(data_value_validator)
    @primitive_field()
    def value(self):
        """
        The type-compatible value to assign to the named parameter. Parameter values may be provided as the result from the evaluation of an expression or a function.
        """

@short_form_field('primary')
@has_fields
class OperationDefinitionImplementation(ToscaPresentation):
    @primitive_field(str)
    def primary(self):
        """
        The optional implementation artifact name (i.e., the primary script file name within a TOSCA CSAR file).  
        
        :rtype: str
        """

    @primitive_list_field(str)
    def dependencies(self):
        """
        The optional ordered list of one or more dependent or secondary implementation artifact name which are referenced by the primary implementation artifact (e.g., a library the script installs or a secondary script).    
        
        :rtype: list of str
        """

@short_form_field('implementation')
@has_fields
@dsl_specification('3.5.13-1', 'tosca-simple-profile-1.0')
class OperationDefinitionForType(ToscaPresentation):
    """
    An operation definition defines a named function or procedure that can be bound to an implementation artifact (e.g., a script).
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_OPERATION_DEF>`__
    """

    @object_field(Description)
    def description(self):
        """
        The optional description string for the associated named operation.
        
        :rtype: :class:`Description`
        """

    @object_field(OperationDefinitionImplementation)
    def implementation(self):
        """
        The optional implementation artifact name (e.g., a script file name within a TOSCA CSAR file).  
        
        :rtype: :class:`OperationDefinitionImplementation`
        """

    @object_dict_field(PropertyDefinition)
    def inputs(self):
        """
        The optional list of input property definitions available to all defined operations for interface definitions that are within TOSCA Node or Relationship Type definitions. This includes when interface definitions are included as part of a Requirement definition in a Node Type.
        
        :rtype: dict of str, :class:`PropertyDefinition`
        """

@short_form_field('implementation')
@has_fields
@dsl_specification('3.5.13-2', 'tosca-simple-profile-1.0')
class OperationDefinitionForTemplate(ToscaPresentation):
    """
    An operation definition defines a named function or procedure that can be bound to an implementation artifact (e.g., a script).
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_OPERATION_DEF>`__
    """

    @object_field(Description)
    def description(self):
        """
        The optional description string for the associated named operation.
        
        :rtype: :class:`Description`
        """

    @object_field(OperationDefinitionImplementation)
    def implementation(self):
        """
        The optional implementation artifact name (e.g., a script file name within a TOSCA CSAR file).  
        
        :rtype: :class:`OperationDefinitionImplementation`
        """

    @object_dict_field(PropertyAssignment)
    def inputs(self):
        """
        The optional list of input property assignments (i.e., parameters assignments) for operation definitions that are within TOSCA Node or Relationship Template definitions. This includes when operation definitions are included as part of a Requirement assignment in a Node Template.
        
        :rtype: dict of str, :class:`PropertyAssignment`
        """
    
@allow_unknown_fields
@has_fields
@dsl_specification('3.5.14-1', 'tosca-simple-profile-1.0')
class InterfaceDefinitionForType(ToscaPresentation):
    """
    An interface definition defines a named interface that can be associated with a Node or Relationship Type.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_INTERFACE_DEF>`__
    """
    
    @field_validator(type_validator('interface type', 'interface_types'))
    @primitive_field(str)
    def type(self):
        """
        Not mentioned in the spec.
        
        :rtype: str
        """

    @object_dict_field(PropertyDefinition)
    def inputs(self):
        """
        The optional list of input property definitions available to all defined operations for interface definitions that are within TOSCA Node or Relationship Type definitions. This includes when interface definitions are included as part of a Requirement definition in a Node Type.
        
        :rtype: dict of str, :class:`PropertyDefinition`
        """

    @object_dict_unknown_fields(OperationDefinitionForType)
    def operations(self):
        pass

    @cachedmethod
    def _get_type(self, context):
        return context.presentation.interface_types.get(self.type) if context.presentation.interface_types is not None else None

    @cachedmethod
    def _get_inputs(self, context):
        return ReadOnlyDict(get_and_override_input_definitions_from_type(context, self))

    @cachedmethod
    def _get_operations(self, context):
        return ReadOnlyDict(get_and_override_operation_definitions_from_type(context, self))
    
    def _validate(self, context):
        super(InterfaceDefinitionForType, self)._validate(context)
        if self.operations:
            for operation in self.operations.itervalues():
                operation._validate(context)

@allow_unknown_fields
@has_fields
@dsl_specification('3.5.14-2', 'tosca-simple-profile-1.0')
class InterfaceDefinitionForTemplate(ToscaPresentation):
    """
    An interface definition defines a named interface that can be associated with a Node or Relationship Type.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_INTERFACE_DEF>`__
    """

    @object_dict_field(PropertyAssignment)
    def inputs(self):
        """
        The optional list of input property assignments (i.e., parameters assignments) for interface definitions that are within TOSCA Node or Relationship Template definitions. This includes when interface definitions are referenced as part of a Requirement assignment in a Node Template.
        
        :rtype: dict of str, :class:`PropertyAssignment`
        """

    @object_dict_unknown_fields(OperationDefinitionForTemplate)
    def operations(self):
        pass
    
    @cachedmethod
    def _get_type(self, context):
        the_type = self._container._get_type(context)
        
        if isinstance(the_type, tuple):
            # In RequirementAssignmentRelationship
            the_type = the_type[0] # This could be a RelationshipTemplate

        interface_definitions = the_type._get_interfaces(context) if the_type is not None else None
        interface_definition = interface_definitions.get(self._name) if interface_definitions is not None else None
        return interface_definition._get_type(context) if interface_definition is not None else None

    def _validate(self, context):
        super(InterfaceDefinitionForTemplate, self)._validate(context)
        if self.operations:
            for operation in self.operations.itervalues():
                operation._validate(context)

@short_form_field('type')
@has_fields
class RequirementDefinitionRelationship(ToscaPresentation):
    @field_validator(type_validator('relationship type', 'relationship_types'))
    @primitive_field(str, required=True)
    def type(self):
        """
        The optional reserved keyname used to provide the name of the Relationship Type for the requirement definition's relationship keyname.
        
        :rtype: str
        """
    
    @object_dict_field(InterfaceDefinitionForType)
    def interfaces(self):
        """
        The optional reserved keyname used to reference declared (named) interface definitions of the corresponding Relationship Type in order to declare additional Property definitions for these interfaces or operations of these interfaces.
        
        :rtype: list of :class:`InterfaceDefinitionForType`
        """

    @cachedmethod
    def _get_type(self, context):
        return context.presentation.relationship_types.get(self.type) if context.presentation.relationship_types is not None else None

@short_form_field('capability')    
@has_fields
@dsl_specification('3.6.2', 'tosca-simple-profile-1.0')
class RequirementDefinition(ToscaPresentation):
    """
    The Requirement definition describes a named requirement (dependencies) of a TOSCA Node Type or Node template which needs to be fulfilled by a matching Capability definition declared by another TOSCA modelable entity. The requirement definition may itself include the specific name of the fulfilling entity (explicitly) or provide an abstract type, along with additional filtering characteristics, that a TOSCA orchestrator can use to fulfill the capability at runtime (implicitly).
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_REQUIREMENT_DEF>`__
    """
    
    @field_validator(type_validator('capability type', 'capability_types'))
    @primitive_field(str, required=True)
    def capability(self):
        """
        The required reserved keyname used that can be used to provide the name of a valid Capability Type that can fulfill the requirement.
        
        :rtype: str
        """

    @field_validator(type_validator('node type', 'node_types'))
    @primitive_field(str)
    def node(self):
        """
        The optional reserved keyname used to provide the name of a valid Node Type that contains the capability definition that can be used to fulfill the requirement.
        
        :rtype: str
        """

    @object_field(RequirementDefinitionRelationship)
    def relationship(self):
        """
        The optional reserved keyname used to provide the name of a valid Relationship Type to construct when fulfilling the requirement.
        
        :rtype: :class:`RequirementDefinitionRelationship`
        """

    @field_getter(data_type_class_getter(Range))
    @primitive_field()
    def occurrences(self):
        """ 	
        The optional minimum and maximum occurrences for the requirement.

        Note: the keyword UNBOUNDED is also supported to represent any positive integer.
        
        :rtype: :class:`Range`
        """

    @cachedmethod
    def _get_type(self, context):
        return context.presentation.capability_types.get(self.capability) if context.presentation.capability_types is not None else None

    @cachedmethod
    def _get_node_type(self, context):
        return context.presentation.node_types.get(self.node)

@short_form_field('type')
@has_fields
@dsl_specification('3.6.1', 'tosca-simple-profile-1.0')
class CapabilityDefinition(ToscaPresentation):
    """
    A capability definition defines a named, typed set of data that can be associated with Node Type or Node Template to describe a transparent capability or feature of the software component the node describes.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_CAPABILITY_DEFN>`__
    """
    
    @field_validator(type_validator('capability type', 'capability_types'))
    @primitive_field(str, required=True)
    def type(self):
        """
        The required name of the Capability Type the capability definition is based upon.
        
        :rtype: str
        """
    
    @object_field(Description)
    def description(self):
        """
        The optional description of the Capability definition.
        
        :rtype: :class:`Description`
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

    @field_validator(list_type_validator('node type', 'node_types'))
    @primitive_list_field(str)
    def valid_source_types(self):
        """
        An optional list of one or more valid names of Node Types that are supported as valid sources of any relationship established to the declared Capability Type.
        
        :rtype: list of str
        """

    @field_getter(data_type_class_getter(Range))
    @primitive_field()
    def occurrences(self):
        """
        The optional minimum and maximum occurrences for the capability. By default, an exported Capability should allow at least one relationship to be formed with it with a maximum of UNBOUNDED relationships.

        Note: the keyword UNBOUNDED is also supported to represent any positive integer.
        
        Note: The spec seems wrong here: the implied default should be [0,UNBOUNDED], not [1,UNBOUNDED], otherwise it would imply that at 1 least one relationship *must* be formed.
        
        :rtype: :class:`Range`
        """

    @cachedmethod
    def _get_type(self, context):
        return context.presentation.capability_types.get(self.type) if context.presentation.capability_types is not None else None
    
    @cachedmethod
    def _get_parent(self, context):
        container_parent = self._container._get_parent(context)
        container_parent_capabilities = container_parent._get_capabilities(context) if container_parent is not None else None
        return container_parent_capabilities.get(self._name) if container_parent_capabilities is not None else None

@has_fields
@dsl_specification('3.5.6', 'tosca-simple-profile-1.0')
class ArtifactDefinition(ToscaPresentation):
    """
    An artifact definition defines a named, typed file that can be associated with Node Type or Node Template and used by orchestration engine to facilitate deployment and implementation of interface operations.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_ARTIFACT_DEF>`__
    """
    
    @field_validator(type_validator('artifact type', 'artifact_types'))
    @primitive_field(str, required=True)
    def type(self):
        """
        The required artifact type for the artifact definition.
        
        :rtype: str
        """

    @primitive_field(str, required=True)
    def file(self):
        """
        The required URI string (relative or absolute) which can be used to locate the artifact's file.
            
        :rtype: str
        """
    
    @field_validator(type_validator('repository', 'repositories'))
    @primitive_field(str)
    def repository(self):
        """
        The optional name of the repository definition which contains the location of the external repository that contains the artifact. The artifact is expected to be referenceable by its file URI within the repository.
        
        :rtype: str
        """

    @object_field(Description)
    def description(self):
        """
        The optional description for the artifact definition.
        
        :rtype: :class:`Description`
        """

    @primitive_field(str)
    def deploy_path(self):
        """
        The file path the associated file would be deployed into within the target node's container.
        
        :rtype: str
        """

    @object_dict_field(PropertyAssignment)
    def properties(self):
        """
        Not mentioned in spec, but is implied.
        
        :rtype: dict of str, :class:`PropertyAssignment`
        """

    @cachedmethod
    def _get_type(self, context):
        return context.presentation.artifact_types.get(self.type) if context.presentation.artifact_types is not None else None

    @cachedmethod
    def _get_repository(self, context):
        return context.presentation.repositories.get(self.repository) if context.presentation.repositories is not None else None

    @cachedmethod
    def _get_property_values(self, context):
        return ReadOnlyDict(get_assigned_and_defined_property_values(context, self))

    @cachedmethod
    def _validate(self, context):
        super(ArtifactDefinition, self)._validate(context)
        self._get_property_values(context)

@has_fields
@dsl_specification('3.7.5', 'tosca-simple-profile-1.0')
class GroupDefinition(ToscaPresentation):
    """
    A group definition defines a logical grouping of node templates, typically for management purposes, but is separate from the application's topology template.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_GROUP_DEF>`__
    """

    @field_validator(type_validator('group type', 'group_types'))
    @primitive_field(str, required=True)
    def type(self):
        """
        The required name of the group type the group definition is based upon.
        
        :rtype: str
        """

    @object_field(Description)
    def description(self):
        """
        The optional description for the group definition.
        
        :rtype: :class:`Description`
        """

    @object_dict_field(PropertyAssignment)
    def properties(self):
        """
        An optional list of property value assignments for the group definition.
        
        :rtype: dict of str, :class:`PropertyAssignment`
        """

    @field_validator(list_type_validator('node template', 'node_templates'))
    @primitive_list_field(str)
    def members(self):
        """
        The optional list of one or more node template names that are members of this group definition.
        
        :rtype: list of str
        """

    @object_dict_field(InterfaceDefinitionForTemplate)
    def interfaces(self):
        """
        An optional list of named interface definitions for the group definition.
        
        :rtype: dict of str, :class:`InterfaceDefinition`
        """

    @cachedmethod
    def _get_type(self, context):
        return context.presentation.group_types.get(self.type) if context.presentation.group_types is not None else None

    @cachedmethod
    def _get_property_values(self, context):
        return ReadOnlyDict(get_assigned_and_defined_property_values(context, self))

    @cachedmethod
    def _get_interfaces(self, context):
        return ReadOnlyDict(get_template_interfaces(context, self, 'group definition'))
    
    def _validate(self, context):
        super(GroupDefinition, self)._validate(context)
        self._get_property_values(context)
        self._get_interfaces(context)

@has_fields
@dsl_specification('3.7.6', 'tosca-simple-profile-1.0')
class PolicyDefinition(ToscaPresentation):
    """
    A policy definition defines a policy that can be associated with a TOSCA topology or top-level entity definition (e.g., group definition, node template, etc.).
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_POLICY_DEF>`__
    """

    @field_validator(type_validator('policy type', 'policy_types'))
    @primitive_field(str, required=True)
    def type(self):
        """
        The required name of the policy type the policy definition is based upon.
        
        :rtype: str
        """

    @object_field(Description)
    def description(self):
        """
        The optional description for the policy definition.
        
        :rtype: :class:`Description`
        """

    @object_dict_field(PropertyAssignment)
    def properties(self):
        """
        An optional list of property value assignments for the policy definition.
        
        :rtype: dict of str, :class:`PropertyAssignment`
        """

    @field_validator(policy_node_template_or_group_validator)
    @primitive_list_field(str)
    def targets(self):
        """
        An optional list of valid Node Templates or Groups the Policy can be applied to.
        
        :rtype: list of str
        """

    @cachedmethod
    def _get_type(self, context):
        return context.presentation.policy_types.get(self.type) if context.presentation.policy_types is not None else None

    @cachedmethod
    def _get_property_values(self, context):
        return ReadOnlyDict(get_assigned_and_defined_property_values(context, self))

    @cachedmethod
    def _get_targets(self, context):
        node_templates, groups = get_policy_targets(context, self)
        return ReadOnlyList(node_templates), ReadOnlyList(groups)

    def _validate(self, context):
        super(PolicyDefinition, self)._validate(context)
        self._get_property_values(context)
