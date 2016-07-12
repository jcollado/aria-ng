
from aria.presentation import Presentation, has_fields, allow_unknown_fields, primitive_field, object_dict_field

@allow_unknown_fields
@has_fields
class PropertyAssignment(Presentation):
    @property
    def value(self):
        return self._raw
    
    @value.setter
    def value(self, value):
        self._raw = value
        
    #TODO

@has_fields
class TriggerAssignment(Presentation):
    @primitive_field(str, required=True)
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
    @primitive_field(str, required=True)
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

