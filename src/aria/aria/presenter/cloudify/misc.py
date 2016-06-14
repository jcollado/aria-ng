
from aria import has_fields, primitive_field, object_dict_field, field_type, field_getter, required_field
from aria.presenter import Presentation
from aria.presenter.tosca_simple import PropertyDefinition

@has_fields
class Output(Presentation):
    @field_type(str)
    @primitive_field
    def description():
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

    @required_field
    @primitive_field
    def value():
        pass

@has_fields
class Relationship(Presentation):
    @required_field
    @field_type(str)
    @primitive_field
    def type():
        """
        :rtype: str
        """

    @field_type(str)
    @primitive_field
    def target():
        """
        :rtype: str
        """

def get_implementation(field, raw):
    if isinstance(raw, basestring):
        return raw
    else:
        return field._get(raw)

@has_fields
class Workflow(Presentation):
    @field_type(str)
    @field_getter(get_implementation)
    @primitive_field
    def implementation():
        """
        :rtype: str
        """

    @field_type(str)
    @primitive_field
    def executor():
        """
        :rtype: str
        """

    @object_dict_field(PropertyDefinition)
    def inputs():
        """
        :rtype: dict of str, :class:`PropertyDefinition`
        """
