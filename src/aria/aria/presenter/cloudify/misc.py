
from aria.presenter import HasRaw, has_properties, property_primitive, property_object_dict, required
from aria.presenter.tosca_simple import PropertyAssignment

@has_properties
class Input(HasRaw):
    @property_primitive
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

@has_properties
class Output(HasRaw):
    @property_primitive
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @required
    @property_object_dict(PropertyAssignment)
    def value(self):
        """
        :class:`PropertyAssignment`
        """

@has_properties
class Relationship(HasRaw):
    @required
    @property_primitive
    def type(self):
        pass

    @property_primitive
    def target(self):
        pass

@has_properties
class Workflow(HasRaw):
    def __init__(self, raw={}):
        super(Workflow, self).__init__({'implementation': raw} if isinstance(raw, basestring) else raw)

    @property_primitive
    def implementation(self):
        pass

    @property_primitive
    def executor(self):
        pass

    @property_object_dict(PropertyAssignment)
    def inputs(self):
        """
        :class:`PropertyAssignment`
        """
    
