
from aria import dsl_specification
from aria.presentation import Presentation, AsIsPresentation, has_fields, short_form_field, primitive_field, object_field, object_dict_field
from .filters import NodeFilter

@dsl_specification('3.5.9', 'tosca-simple-profile-1.0')
class PropertyAssignment(AsIsPresentation):
    """
    This section defines the grammar for assigning values to named properties within TOSCA Node and Relationship templates that are defined in their corresponding named types.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_PROPERTY_VALUE_ASSIGNMENT>`__
    """

@short_form_field('type')
@has_fields
class RequirementAssignmentRelationship(Presentation):
    @primitive_field(str)
    def type(self):
        """
        The optional reserved keyname used to provide the name of the Relationship Type for the requirement assignment's relationship keyname.
        
        :rtype: str
        """

    #@object_dict_field(InterfaceDefinition)
    def properties(self):
        """
        The optional reserved keyname used to reference declared (named) interface definitions of the corresponding Relationship Type in order to provide Property assignments for these interfaces or operations of these interfaces.
        
        :rtype: dict of str, :class:`InterfaceDefinition`
        """

@short_form_field('node')
@has_fields
@dsl_specification('3.7.2', 'tosca-simple-profile-1.0')
class RequirementAssignment(Presentation):
    """
    A Requirement assignment allows template authors to provide either concrete names of TOSCA templates or provide abstract selection criteria for providers to use to find matching TOSCA templates that are used to fulfill a named requirement's declared TOSCA Node Type.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_REQUIREMENT_ASSIGNMENT>`__
    """
    
    # The example in 3.7.2.2.2 shows unknown fields in addition to these, but is this a mistake?

    @primitive_field(str)
    def capability(self):
        """
        The optional reserved keyname used to provide the name of either a:

        * Capability definition within a target node template that can fulfill the requirement.
        * Capability Type that the provider will use to select a type-compatible target node template to fulfill the requirement at runtime. 
        
        :rtype: str
        """

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

@has_fields
@dsl_specification('3.7.1', 'tosca-simple-profile-1.0')
class CapabilityAssignment(Presentation):
    """
    A capability assignment allows node template authors to assign values to properties and attributes for a named capability definition that is part of a Node Template's type definition.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_CAPABILITY_ASSIGNMENT>`__
    """
    
    #TODO

@has_fields
@dsl_specification('3.5.11', 'tosca-simple-profile-1.0')
class AttributeAssignment(Presentation):
    """
    This section defines the grammar for assigning values to named attributes within TOSCA Node and Relationship templates which are defined in their corresponding named types.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_ATTRIBUTE_VALUE_ASSIGNMENT>`__
    """
    
    #TODO
