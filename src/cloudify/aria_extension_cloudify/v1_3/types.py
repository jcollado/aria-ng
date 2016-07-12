
from .definitions import InterfaceDefinition, PropertyDefinition
from aria import dsl_specification
from aria.presentation import Presentation, has_fields, primitive_field, object_dict_field, field_validator, derived_from_validator

@has_fields
@dsl_specification('node-types', 'cloudify-1.3')
class NodeType(Presentation):
    """
    node_types are used for defining common properties and behaviors for node-templates. node-templates can then be created based on these types, inheriting their definitions.

    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-node-types/>`__
    """

    @primitive_field(str)
    def description(self):
        """
        Not mentioned in the spec.
        
        :rtype: str
        """

    @field_validator(derived_from_validator('node_types'))
    @primitive_field(str)
    def derived_from(self):
        """
        A string referencing a parent type.
        
        :rtype: str
        """

    @object_dict_field(InterfaceDefinition)
    def interfaces(self):
        """
        A dictionary of node interfaces.
        
        :rtype: dict of str, :class:`InterfaceDefinition`
        """
    
    @object_dict_field(PropertyDefinition)
    def properties(self):
        """
        A dictionary of node interfaces.
        
        :rtype: dict of str, :class:`PropertyDefinition`
        """

@has_fields
@dsl_specification('relationships-2', 'cloudify-1.3')
class RelationshipType(Presentation):
    """
    You can declare your own relationship types in the relationships section in the blueprint. This is useful when you want to change the default implementation of how nodes interact.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-relationships/#declaring-relationship-types>`__
    """

    @primitive_field(str)
    def description(self):
        """
        Not mentioned in the spec.
        
        :rtype: str
        """

    @field_validator(derived_from_validator('relationship_types'))
    @primitive_field(str)
    def derived_from(self):
        """
        The relationship type from which the new relationship is derived.
        
        :rtype: str
        """

    @object_dict_field(InterfaceDefinition)
    def source_interfaces(self):
        """
        A dict of interfaces.
        
        :rtype: dict of str, :class:`InterfaceDefinition`
        """

    @object_dict_field(InterfaceDefinition)
    def target_interfaces(self):
        """
        A dict of interfaces.
        
        :rtype: dict of str, :class:`InterfaceDefinition`
        """
    
    @primitive_field(str, allowed=('all_to_all', 'all_to_one'))
    def connection_type(self):
        """
        valid values: all_to_all and all_to_one
        
        :rtype: str
        """

@has_fields
@dsl_specification('policy-types', 'cloudify-1.3')
class PolicyType(Presentation):
    """
    policies provide a way of analyzing a stream of events that correspond to a group of nodes (and their instances).
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-policy-types/>`__.
    """

    @primitive_field(str)
    def description(self):
        """
        Not mentioned in the spec.
        
        :rtype: str
        """

    @primitive_field(str, required=True)
    def source(self):
        """
        The policy trigger implementation source (URL or a path relative to the blueprint root directory).
        
        :rtype: str
        """

    @object_dict_field(PropertyDefinition)
    def properties(self):
        """
        Optional properties schema for the policy type.
        
        :rtype: dict of str, :class:`PropertyDefinition`
        """

@has_fields
@dsl_specification('data-types', 'cloudify-1.3')
class DataType(Presentation):
    """
    data_types are useful for grouping together and re-using a common set of properties, along with their types and default values.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-data-types/>`__.
    """

    @primitive_field(str)
    def description(self):
        """
        Description for the data type.
        
        :rtype: str
        """

    @object_dict_field(PropertyDefinition)
    def properties(self):
        """
        Dictionary of the data type properties.
        
        :rtype: dict of str, :class:`PropertyDefinition`
        """

    @field_validator(derived_from_validator('data_types'))
    @primitive_field(str)
    def derived_from(self):
        """
        Parent data type.
        
        :rtype: str
        """
