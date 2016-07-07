
from .... import has_fields, primitive_field, object_dict_field, required_field, field_type
from ... import Presentation
from ...tosca.v1_0 import PropertyAssignment

@has_fields
class TriggerAssignment(Presentation):
    @required_field
    @field_type(str)
    @primitive_field
    def type(self):
        """
        Trigger type.
        
        :rtype: str
        """

    @object_dict_field(PropertyAssignment)
    def properties(self):
        """
        Optional parameters that will be passed to the trigger.
        
        :rtype: dict of str, :class:`PropertyAssignment`
        """

@has_fields
class PolicyAssignment(Presentation):
    @required_field
    @field_type(str)
    @primitive_field
    def type(self):
        """
        Policy type.
        
        :rtype: str
        """

    @object_dict_field(PropertyAssignment)
    def properties(self):
        """
        Optional properties for configuring the policy.
        
        :rtype: dict of str, :class:`PropertyAssignment`
        """

    @object_dict_field(TriggerAssignment)
    def triggers(self):
        """
        A dict of triggers.
        
        :rtype: dict of str, :class:`TriggerAssignment`
        """

