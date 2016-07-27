
from .presentation import ToscaPresentation
from .filters import NodeFilter
from .definitions import InterfaceDefinitionForTemplate
from .property_assignment import PropertyAssignment
from .field_validators import node_template_or_type_validator, relationship_template_or_type_validator, capability_definition_or_type_validator
from .utils.properties import get_assigned_and_defined_property_values
from .utils.interfaces import get_template_interfaces
from aria import dsl_specification
from aria.presentation import has_fields, short_form_field, primitive_field, object_field, object_dict_field, field_validator

@short_form_field('type')
@has_fields
class RequirementAssignmentRelationship(ToscaPresentation):
    @field_validator(relationship_template_or_type_validator)
    @primitive_field(str)
    def type(self):
        """
        The optional reserved keyname used to provide the name of the Relationship Type for the requirement assignment's relationship keyname.
        
        :rtype: str
        """

    @object_dict_field(PropertyAssignment)
    def properties(self):
        """
        The spec doesn't mention this but shows it in examples.
        
        :rtype: dict of str, :class:`PropertyAssignment`
        """

    @object_dict_field(InterfaceDefinitionForTemplate)
    def interfaces(self):
        """
        The optional reserved keyname used to reference declared (named) interface definitions of the corresponding Relationship Type in order to provide Property assignments for these interfaces or operations of these interfaces.
        
        :rtype: dict of str, :class:`InterfaceDefinitionForTemplate`
        """

    def _get_type(self, context):
        the_type = context.presentation.relationship_types.get(self.type)
        if the_type is None:
            the_type = context.presentation.relationship_templates.get(self.type)
        return the_type

    def _get_properties(self, context):
        return get_assigned_and_defined_property_values(context, self)

    def _get_interfaces(self, context):
        return get_template_interfaces(context, self, 'requirement assignment')

    def _validate(self, context):
        super(RequirementAssignmentRelationship, self)._validate(context)
        self._get_properties(context)
        self._get_interfaces(context)

@short_form_field('node')
@has_fields
@dsl_specification('3.7.2', 'tosca-simple-profile-1.0')
class RequirementAssignment(ToscaPresentation):
    """
    A Requirement assignment allows template authors to provide either concrete names of TOSCA templates or provide abstract selection criteria for providers to use to find matching TOSCA templates that are used to fulfill a named requirement's declared TOSCA Node Type.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_REQUIREMENT_ASSIGNMENT>`__
    """
    
    # The example in 3.7.2.2.2 shows unknown fields in addition to these, but is this a mistake?

    @field_validator(capability_definition_or_type_validator)
    @primitive_field(str)
    def capability(self):
        """
        The optional reserved keyname used to provide the name of either a:

        * Capability definition within a target node template that can fulfill the requirement.
        * Capability Type that the provider will use to select a type-compatible target node template to fulfill the requirement at runtime. 
        
        :rtype: str
        """

    @field_validator(node_template_or_type_validator)
    @primitive_field(str)
    def node(self):
        """
        The optional reserved keyname used to identify the target node of a relationship. Specifically, it is used to provide either a:

        * Node Template name that can fulfill the target node requirement.
        * Node Type name that the provider will use to select a type-compatible node template to fulfill the requirement at runtime. 
        
        :rtype: str
        """

    @object_field(RequirementAssignmentRelationship)
    def relationship(self):
        """
        The optional reserved keyname used to provide the name of either a:

        * Relationship Template to use to relate the source node to the (capability in the) target node when fulfilling the requirement.
        * Relationship Type that the provider will use to select a type-compatible relationship template to relate the source node to the target node at runtime. 
        
        :rtype: :class:`RequirementRelationshipAssignment`
        """

    @object_dict_field(NodeFilter)
    def node_filter(self):
        """
        The optional filter definition that TOSCA orchestrators or providers would use to select a type-compatible target node that can fulfill the associated abstract requirement at runtime.
        
        :rtype: dict of str, :class:`NodeFilter`
        """
    
    def _get_node(self, context):
        node = self.node
        if node in context.presentation.node_templates:
            return context.presentation.node_templates[node], 'node_template'
        elif node in context.presentation.node_types:
            return context.presentation.node_types[node], 'node_type'
        return None, None

    def _get_capability(self, context):
        capability = self.capability
        
        if capability is not None:
            node, node_variant = self._get_node(context)
            capability_definitions_or_assignments = node._get_capabilities(context) if node is not None else None
            
            if (capability_definitions_or_assignments is not None) and (capability in capability_definitions_or_assignments):
                if node_variant == 'node_template':
                    return capability_definitions_or_assignments[capability], 'capability_assignment'
                else:
                    return capability_definitions_or_assignments[capability], 'capability_definition'
        
            capability_types = context.presentation.capability_types
            if (context.presentation.capability_types is not None) and (capability in capability_types):
                return capability_types[capability], 'capability_type'
        
        return None, None

@has_fields
@dsl_specification('3.5.11', 'tosca-simple-profile-1.0')
class AttributeAssignment(ToscaPresentation):
    """
    This section defines the grammar for assigning values to named attributes within TOSCA Node and Relationship templates which are defined in their corresponding named types.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_ATTRIBUTE_VALUE_ASSIGNMENT>`__
    """
    
    #TODO

@has_fields
@dsl_specification('3.7.1', 'tosca-simple-profile-1.0')
class CapabilityAssignment(ToscaPresentation):
    """
    A capability assignment allows node template authors to assign values to properties and attributes for a named capability definition that is part of a Node Template's type definition.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_CAPABILITY_ASSIGNMENT>`__
    """
    
    @object_dict_field(PropertyAssignment)
    def properties(self):
        """
        An optional list of property definitions for the Capability definition.
        
        :rtype: dict of str, :class:`PropertyAssignment`
        """

    @object_dict_field(AttributeAssignment)
    def attributes(self):
        """
        An optional list of attribute definitions for the Capability definition.
        
        :rtype: dict of str, :class:`AttributeAssignment`
        """

    def _get_type(self, context):
        node_type = self._container._get_type(context)
        capability_definitions = node_type._get_capabilities(context) if node_type is not None else None
        capability_definition = capability_definitions.get(self._name) if capability_definitions is not None else None
        return capability_definition._get_type(context) if capability_definition is not None else None

    def _get_properties(self, context):
        return get_assigned_and_defined_property_values(context, self)

    def _validate(self, context):
        super(CapabilityAssignment, self)._validate(context)
        self._get_properties(context)
