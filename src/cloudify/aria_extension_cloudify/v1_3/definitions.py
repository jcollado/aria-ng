
from aria import dsl_specification
from aria.presentation import Presentation, has_fields, primitive_field, primitive_list_field, object_dict_field, ReadOnlyDict
from aria_extension_tosca.v1_0 import PropertyAssignment
from .assignments import PolicyAssignment
from .misc import Operation

@has_fields
@dsl_specification('interfaces', 'cloudify-1.3')
class InterfaceDefinition(Presentation):
    """
    Interfaces provide a way to map logical tasks to executable operations.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-interfaces/>`__.
    """

    def __init__(self, *args, **kwargs):
        super(InterfaceDefinition, self).__init__(*args, **kwargs)
        self._allow_unknown_fields = True

    @property
    def operations(self):
        """
        :rtype: dict of str, :class:`Operation`
        """
        return ReadOnlyDict([(k, Operation(raw=v)) for k, v in self._raw.iteritems()])

@has_fields
@dsl_specification('groups', 'cloudify-1.3')
class GroupDefinition(Presentation):
    """
    Groups provide a way of configuring shared behavior for different sets of node_templates.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-groups/>`__.
    """

    @primitive_list_field(str, required=True)
    def members(self):
        """
        A list of group members. Members are node template names or other group names. 
        
        :rtype: list of str
        """

    @object_dict_field(PolicyAssignment)
    def policies(self):
        """
        A dict of policies. 
        
        :rtype: dict of str, :class:`PolicyAssignment`
        """

@has_fields
@dsl_specification('policies', 'cloudify-1.3')
class PolicyDefinition(Presentation):
    """
    Policies provide a way of configuring reusable behavior by referencing groups for which a policy applies.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-policies/>`__.    
    """
    
    @primitive_field(str, required=True)
    def type(self):
        """
        The policy type.
        
        :rtype: str
        """

    @object_dict_field(PropertyAssignment)
    def properties(self):
        """
        The specific policy properties. The properties schema is defined by the policy type.
        
        :rtype: dict of str, :class:`PropertyAssignment`
        """

    @primitive_list_field(str, required=True)
    def targets(self):
        """
        A list of group names. The policy will be applied on the groups specified in this list. 
        
        :rtype: list of str
        """
