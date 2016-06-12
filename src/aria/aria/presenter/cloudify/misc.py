
from aria import has_fields, primitive_field, object_dict_field, field_type, required_field
from aria.presenter import Presentation
from aria.presenter.tosca_simple import PropertyAssignment

@has_fields
class Input(Presentation):
    @field_type(str)
    @primitive_field
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

@has_fields
class Output(Presentation):
    @field_type(str)
    @primitive_field
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

    @required_field
    @object_dict_field(PropertyAssignment)
    def value(self):
        """
        :rtype: dict of str, :class:`PropertyAssignment`
        """

@has_fields
class Relationship(Presentation):
    @required_field
    @field_type(str)
    @primitive_field
    def type(self):
        """
        :rtype: str
        """

    @field_type(str)
    @primitive_field
    def target(self):
        """
        :rtype: str
        """

@has_fields
class Workflow(Presentation):
    def __init__(self, raw={}):
        super(Workflow, self).__init__({'implementation': raw} if isinstance(raw, basestring) else raw)

    @field_type(str)
    @primitive_field
    def implementation(self):
        """
        :rtype: str
        """

    @field_type(str)
    @primitive_field
    def executor(self):
        """
        :rtype: str
        """

    @object_dict_field(PropertyAssignment)
    def inputs(self):
        """
        :rtype: dict of str, :class:`PropertyAssignment`
        """
