
from .assignments import PropertyAssignment
from aria import dsl_specification
from aria.presentation import Presentation, has_fields, short_form_field, primitive_field, object_field, object_dict_field 
from tosca import Version

@has_fields
@dsl_specification('outputs', 'cloudify-1.3')
class Output(Presentation):
    """
    Outputs provide a way of exposing global aspects of a deployment. When deployed, a blueprint can expose specific outputs of that deployment - for instance, an endpoint of a server or any other runtime or static information of a specific resource.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-outputs/>`__.
    """
    
    @primitive_field(str)
    def description(self):
        """
        An optional description for the output.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

    @primitive_field(required=True)
    def value(self):
        """
        The output value. Can be anything from a simple value (e.g. port) to a complex value (e.g. hash with values). Output values can contain hardcoded values, inputs, properties and attributes.
        """

@short_form_field('implementation')
@has_fields
class Operation(Presentation):
    @primitive_field(str, required=True)
    def implementation(self):
        """
        The script or plugin task name to execute.
        
        :rtype: str
        """

    @object_dict_field(PropertyAssignment)
    def inputs(self):
        """
        Schema of inputs that will be passed to the implementation as kwargs.
        
        :rtype: dict of str, :class:`PropertyAssignment`
        """

    @primitive_field(str)
    def executor(self):
        """
        Valid values: central_deployment_agent, host_agent.
        
        :rtype: str
        """

    @primitive_field(str)
    def max_retries(self):
        """
        Maximum number of retries for a task. -1 means infinite retries (Default: task_retries in manager blueprint Cloudify Manager Type for remote workflows and task_retries workflow configuration for local workflows).
        
        :rtype: int
        """

    @primitive_field(int)
    def retry_interval(self):
        """
        Minimum wait time (in seconds) in between task retries (Default: task_retry_interval in manager blueprint Cloudify Manager Type for remote workflows and task_retry_interval workflow configuration for local workflows).
        
        :rtype: int
        """

@short_form_field('mapping')
@has_fields
@dsl_specification('workflows', 'cloudify-1.3')
class Workflow(Presentation):
    """
    Workflows define a set of tasks that can be executed on a node or a group of nodes, and the execution order of these tasks, serially or in parallel. A task may be an operation (implemented by a plugin), but it may also be other actions, including arbitrary code.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-workflows/>`__.
    """

    @primitive_field(str, required=True)
    def mapping(self):
        """
        A path to the method implementing this workflow (In the "Simple mapping" format this value is set without explicitly using the "mapping" key)
        
        :rtype: str
        """

    @object_dict_field(PropertyAssignment)
    def parameters(self):
        """
        A map of parameters to be passed to the workflow implementation
        
        :rtype: dict of str, :class:`PropertyAssignment`
        """
    

@has_fields
@dsl_specification('plugins', 'cloudify-1.3')
class Plugin(Presentation):
    """
    The instances key is used for configuring the deployment characteristics of the node template.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-plugins/>`__.
    """

    @primitive_field(str, required=True)
    def executor(self):
        """
        Where to execute the plugin's operations. Valid Values: central_deployment_agent, host_agent.
        
        :rtype: str
        """

    @primitive_field(str)
    def source(self):
        """
        Where to retrieve the plugin from. Could be either a path relative to the plugins dir inside the blueprint's root dir or a url. If install is false, source is redundant. If install is true, source (or package_name) is mandatory.
        
        :rtype: str
        """

    @primitive_field(str)
    def install_arguments(self):
        """
        Optional arguments passed to the 'pip install' command created for the plugin installation
        
        :rtype: str        
        """

    @primitive_field(bool, default=True)
    def install(self):
        """
        Whether to install the plugin or not as it might already be installed as part of the agent. Defaults to true. (Supported since: cloudify_dsl_1_1)
        
        :rtype: bool
        """

    @primitive_field(str)
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

    @primitive_field(str)
    def supported_platform(self):
        """
        Managed plugin supported platform (e.g. linux_x86_64). (Supported since: cloudify_dsl_1_2)
        
        :rtype: str
        """

    @primitive_field(str)
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

    @primitive_field(str)
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
    
    @primitive_field(int, default=1)
    def default_instances(self):
        """
        The number of node-instances this node template will have.
        
        :rtype: int
        """
    
    @primitive_field(int, default=0)
    def min_instances(self):
        """
        The minimum number of allowed node instances. (Not enforced by scale workflow.)
        
        :rtype: int
        """
        
    @primitive_field(int, default=-1)
    def max_instances(self):
        """
        The maximum number of allowed node instances. (Not enforced by scale workflow.)
        
        UNBOUNDED may be used literally as the value for max_instances. Internally, it is stored as -1, which may also be used.
        
        :rtype: int
        """

@has_fields
@dsl_specification('policy-triggers', 'cloudify-1.3')
class PolicyTrigger(Presentation):
    """
    policy_triggers specify the implementation of actions invoked by policies and declare the properties that define the trigger's behavior.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-policy-triggers/>`__.
    """

    @primitive_field(str, required=True)
    def source(self):
        """
        The policy trigger implementation source (URL or a path relative to the blueprint root directory).
        
        :rtype: str
        """

    @object_dict_field(PropertyAssignment)
    def parameters(self):
        """
        Optional parameters schema for the policy trigger.
        
        :rtype: dict of str, :class:`PropertyAssignment`
        """
