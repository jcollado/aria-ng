
from ... import has_fields, primitive_field, object_field, object_dict_field, field_type, field_getter, required_field
from .. import Presentation
from ..tosca import PropertyDefinition, Version

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
class Operation(Presentation):
    @field_type(str)
    @primitive_field
    def description():
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

    @field_type(str)
    @field_getter(get_implementation)
    @primitive_field
    def implementation():
        """
        :rtype: str
        """

    @field_type(str)
    @primitive_field
    def mapping():
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

    @object_dict_field(PropertyDefinition)
    def parameters():
        """
        :rtype: dict of str, :class:`PropertyDefinition`
        """

@has_fields
class Plugin(Presentation):
    @field_type(str)
    @primitive_field
    def source():
        """
        :rtype: str
        """

    @field_type(str)
    @primitive_field
    def executor():
        """
        :rtype: str
        """

    @field_type(bool)
    @primitive_field
    def install():
        """
        :rtype: bool
        """

    @primitive_field
    def install_arguments():
        """
        """

    @field_type(str)
    @primitive_field
    def package_name():
        """
        :rtype: str
        """

    @object_field(Version)
    def package_version():
        """
        :rtype: :class:`Version`
        """

    @field_type(str)
    @primitive_field
    def supported_platform():
        """
        :rtype: str
        """

    @field_type(str)
    @primitive_field
    def distribution():
        """
        :rtype: str
        """

    @object_field(Version)
    def distribution_version():
        """
        :rtype: :class:`Version`
        """

    @field_type(str)
    @primitive_field
    def distribution_release():
        """
        :rtype: str
        """

@has_fields
class Instances(Presentation):
    @field_type(int)
    @primitive_field
    def deploy():
        """
        :rtype: int
        """
