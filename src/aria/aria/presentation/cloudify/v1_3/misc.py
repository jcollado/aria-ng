
from .... import has_fields, primitive_field, object_field, object_dict_field, field_type, field_default, field_getter, required_field, dsl_specification
from ... import Presentation
from ...tosca.v1_0 import PropertyDefinition, Version

@has_fields
@dsl_specification('outputs', 'cloudify-1.3')
class Output(Presentation):
    """
    Outputs provide a way of exposing global aspects of a deployment. When deployed, a blueprint can expose specific outputs of that deployment - for instance, an endpoint of a server or any other runtime or static information of a specific resource.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-outputs/>`__.
    """
    
    @field_type(str)
    @primitive_field
    def description(self):
        """
        An optional description for the output.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

    @required_field
    @primitive_field
    def value(self):
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
    @field_getter(get_implementation)
    @primitive_field
    def implementation(self):
        """
        The script or plugin task name to execute.
        
        :rtype: str
        """

    @object_dict_field(PropertyDefinition)
    def inputs(self):
        """
        Schema of inputs that will be passed to the implementation as kwargs.
        
        :rtype: dict of str, :class:`PropertyDefinition`
        """

    @field_type(str)
    @primitive_field
    def executor(self):
        """
        Valid values: central_deployment_agent, host_agent.
        
        :rtype: str
        """

    @field_type(int)
    @primitive_field
    def max_retries(self):
        """
        Maximum number of retries for a task. -1 means infinite retries (Default: task_retries in manager blueprint Cloudify Manager Type for remote workflows and task_retries workflow configuration for local workflows).
        
        :rtype: int
        """

    @field_type(int)
    @primitive_field
    def retry_interval(self):
        """
        Minimum wait time (in seconds) in between task retries (Default: task_retry_interval in manager blueprint Cloudify Manager Type for remote workflows and task_retry_interval workflow configuration for local workflows).
        
        :rtype: int
        """

def get_mapping(field, raw):
    if isinstance(raw, basestring):
        return raw
    else:
        return field._get(raw)

@has_fields
@dsl_specification('workflows', 'cloudify-1.3')
class Workflow(Presentation):
    """
    Workflows define a set of tasks that can be executed on a node or a group of nodes, and the execution order of these tasks, serially or in parallel. A task may be an operation (implemented by a plugin), but it may also be other actions, including arbitrary code.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-workflows/>`__.
    """

    @field_type(str)
    @field_getter(get_mapping)
    @primitive_field
    def mapping(self):
        """
        A path to the method implementing this workflow (In the "Simple mapping" format this value is set without explicitly using the "mapping" key)
        
        :rtype: str
        """

    @object_dict_field(PropertyDefinition)
    def parameters(self):
        """
        A map of parameters to be passed to the workflow implementation
        
        :rtype: dict of str, :class:`PropertyDefinition`
        """
    

@has_fields
@dsl_specification('plugins', 'cloudify-1.3')
class Plugin(Presentation):
    """
    The instances key is used for configuring the deployment characteristics of the node template.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-plugins/>`__.
    """

    @required_field
    @field_type(str)
    @primitive_field
    def executor(self):
        """
        Where to execute the plugin's operations. Valid Values: central_deployment_agent, host_agent.
        
        :rtype: str
        """

    @field_type(str)
    @primitive_field
    def source(self):
        """
        Where to retrieve the plugin from. Could be either a path relative to the plugins dir inside the blueprint's root dir or a url. If install is false, source is redundant. If install is true, source (or package_name) is mandatory.
        
        :rtype: str
        """

    @field_type(str)
    @primitive_field
    def install_arguments(self):
        """
        Optional arguments passed to the 'pip install' command created for the plugin installation
        
        :rtype: str        
        """

    @field_default(True)
    @field_type(bool)
    @primitive_field
    def install(self):
        """
        Whether to install the plugin or not as it might already be installed as part of the agent. Defaults to true. (Supported since: cloudify_dsl_1_1)
        
        :rtype: bool
        """

    @field_type(str)
    @primitive_field
    def package_name(self):
        """
        Managed plugin package name. (Supported since: cloudify_dsl_1_2) If install is false, pacakge_name is redundant. If install is true, package_name (or source) is mandatory.
        
        :rtype: str
        """

    @object_field(Version)
    def package_version(self):
        """
        Managed plugin package version. (Supported since: cloudify_dsl_1_2)
        
        :rtype: :class:`Version`
        """

    @field_type(str)
    @primitive_field
    def supported_platform(self):
        """
        Managed plugin supported platform (e.g. linux_x86_64). (Supported since: cloudify_dsl_1_2)
        
        :rtype: str
        """

    @field_type(str)
    @primitive_field
    def distribution(self):
        """
        Managed plugin distribution. (Supported since: cloudify_dsl_1_2)
        
        :rtype: str
        """

    @object_field(Version)
    def distribution_version(self):
        """
        Managed plugin distribution version. (Supported since: cloudify_dsl_1_2)
        
        :rtype: :class:`Version`
        """

    @field_type(str)
    @primitive_field
    def distribution_release(self):
        """
        Managed plugin distribution release. (Supported since: cloudify_dsl_1_2)
        
        :rtype: str
        """

@has_fields
class Scalable(Presentation):
    """
    The capabilities.scalable.properties key is used for configuring the deployment characteristics of the node template.
    """
    
    @field_default(1)
    @field_type(int)
    @primitive_field
    def default_instances(self):
        """
        The number of node-instances this node template will have.
        
        :rtype: int
        """
    
    @field_default(0)
    @field_type(int)
    @primitive_field
    def min_instances(self):
        """
        The minimum number of allowed node instances. (Not enforced by scale workflow.)
        
        :rtype: int
        """
        
    @field_default(-1)
    @field_type(int)
    @primitive_field
    def max_instances(self):
        """
        The maximum number of allowed node instances. (Not enforced by scale workflow.)
        
        UNBOUNDED may be used literally as the value for max_instances. Internally, it is stored as -1, which may also be used.
        
        :rtype: int
        """
