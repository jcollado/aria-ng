
from ... import has_fields, primitive_field, object_field, object_dict_field, field_type, field_default, field_getter, required_field, tosca_specification
from .. import Presentation
from ..tosca import PropertyDefinition, Version

@has_fields
@tosca_specification('outputs', spec='cloudify-1.3')
class Output(Presentation):
    """
    Outputs provide a way of exposing global aspects of a deployment. When deployed, a blueprint can expose specific outputs of that deployment - for instance, an endpoint of a server or any other runtime or static information of a specific resource.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-outputs/>`__.
    """
    
    @field_type(str)
    @primitive_field
    def description():
        """
        An optional description for the output.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

    @required_field
    @primitive_field
    def value():
        """
        The output value. Can be anything from a simple value (e.g. port) to a complex value (e.g. hash with values). Output values can contain hardcoded values, inputs, properties and attributes.
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

    @field_type(int)
    @primitive_field
    def max_retries():
        """
        :rtype: int
        """

    @field_type(int)
    @primitive_field
    def retry_interval():
        """
        :rtype: int
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
@tosca_specification('node-templates', spec='cloudify-1.2')
class Instances(Presentation):
    """
    The instances key is used for configuring the deployment characteristics of the node template.
    
    See the `Cloudify DSL v1.2 specification <http://docs.getcloudify.org/3.3.1/blueprints/spec-node-templates/>`__.
    """
    
    @field_default(1)
    @field_type(int)
    @primitive_field
    def deploy():
        """
        The number of node-instances this node template will have.
        
        :rtype: int
        """

@has_fields
class Scalable(Presentation):
    """
    The capabilities.scalable.properties key is used for configuring the deployment characteristics of the node template.
    """
    
    @field_default(1)
    @field_type(int)
    @primitive_field
    def default_instances():
        """
        The number of node-instances this node template will have.
        
        :rtype: int
        """
    
    @field_default(0)
    @field_type(int)
    @primitive_field
    def min_instances():
        """
        The minimum number of allowed node instances. (Not enforced by scale workflow.)
        
        :rtype: int
        """
        
    @field_default(-1)
    @field_type(int)
    @primitive_field
    def max_instances():
        """
        The maximum number of allowed node instances. (Not enforced by scale workflow.)
        
        UNBOUNDED may be used literally as the value for max_instances. Internally, it is stored as -1, which may also be used.
        
        :rtype: int
        """
