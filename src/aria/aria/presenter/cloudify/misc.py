
from aria.presenter import Presentation, has_fields, primitive_field, object_dict_field, required_field
from aria.presenter.tosca_simple import PropertyAssignment

@has_fields
class Input(Presentation):
    @primitive_field
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

@has_fields
class Output(Presentation):
    @primitive_field
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @required_field
    @object_dict_field(PropertyAssignment)
    def value(self):
        """
        :class:`PropertyAssignment`
        """

@has_fields
class Relationship(Presentation):
    @required_field
    @primitive_field
    def type(self):
        pass

    @primitive_field
    def target(self):
        pass

@has_fields
class Workflow(Presentation):
    def __init__(self, raw={}):
        super(Workflow, self).__init__({'implementation': raw} if isinstance(raw, basestring) else raw)

    @primitive_field
    def implementation(self):
        pass

    @primitive_field
    def executor(self):
        pass

    @object_dict_field(PropertyAssignment)
    def inputs(self):
        """
        :class:`PropertyAssignment`
        """
    
