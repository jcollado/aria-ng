
from aria import dsl_specification, has_validated_properties, validated_property, property_type, property_default, property_status, required_property
import tosca, tosca.datatypes.network, tosca.datatypes.compute

@has_validated_properties
@dsl_specification('5.4.1', 'tosca-simple-profile-1.0')
class Root(object):
    """
    This is the default (root) TOSCA Capability Type definition that all other TOSCA Capability Types derive from.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_CAPABILITIES_ROOT>`__
    """

@has_validated_properties
@dsl_specification('5.4.2', 'tosca-simple-profile-1.0')
class Node(Root):
    """
    The Node capability indicates the base capabilities of a TOSCA Node Type.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_CAPABILITIES_NODE>`__
    """

    SHORTHAND_NAME = 'Node'
    TYPE_QUALIFIED_NAME = 'tosca:Node'
    TYPE_URI = 'tosca.capabilities.Node'

@has_validated_properties
@dsl_specification('5.4.3', 'tosca-simple-profile-1.0')
class Container(Root):
    """
    The Container capability, when included on a Node Type or Template definition, indicates that the node can act as a container for (or a host for) one or more other declared Node Types.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_CAPABILITIES_CONTAINER>`__
    """

    SHORTHAND_NAME = 'Container'
    TYPE_QUALIFIED_NAME = 'tosca:Container'
    TYPE_URI = 'tosca.capabilities.Container'

    @property_type(tosca.Integer)
    @validated_property
    def num_cpus(self):
        """
        Number of (actual or virtual) CPUs associated with the Compute node.
        """

    @property_type(tosca.Frequency)
    @validated_property
    def cpu_frequency(self):
        """
        Specifies the operating frequency of CPU's core. This property expresses the expected frequency of one (1) CPU as provided by the property "num_cpus".
        """

    @property_type(tosca.Size)
    @validated_property
    def disk_size(self):
        """
        Size of the local disk available to applications running on the Compute node (default unit is MB).
        """

    @property_type(tosca.Size)
    @validated_property
    def mem_size(self):
        """
        Size of memory available to applications running on the Compute node (default unit is MB).
        """

@has_validated_properties
@dsl_specification('8.2.1', 'tosca-simple-nfv-1.0')
class _Architecture(Container):
    """
    Enhance compute architecture capability that needs to be typically use for performance sensitive NFV workloads.
    
    See the `TOSCA Simple Profile for NFV v1.0 specification <http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/tosca-nfv-v1.0.html#DEFN_TYPE_CAPABILITIES_CONTAINER>`__
    """

    SHORTHAND_NAME = 'Compute.Container.Architecture'
    TYPE_QUALIFIED_NAME = 'tosca:Compute.Container.Architecture'
    TYPE_URI = 'tosca.capabilities.Compute.Container.Architecture' # mismatch with TOSCA Simple Profile, where we don't have Compute.Container, just Container

    @property_type(str)
    @validated_property
    def mem_page_size(self):
        """
        Describe page size of the VM:

        * small page size is typically 4KB
        * large page size is typically 2MB
        * any page size maps to system default
        * custom MB value: sets TLB size to this specific value
        """

    @property_type(tosca.datatypes.compute.CPUAllocation)
    @validated_property
    def cpu_allocation(self):
        """
        Describes CPU allocation requirements like dedicated CPUs (cpu pinning), socket count, thread count, etc.
        """

    @property_type(tosca.Integer)
    @validated_property
    def numa_node_count(self):
        """
        Specifies the symmetric count of NUMA nodes to expose to the VM. vCPU and Memory equally split across this number of NUMA.

        NOTE: the map of numa_nodes should not be specified. 
        """

    @property_type(tosca.Map(tosca.datatypes.compute.NUMA))
    @validated_property
    def numa_nodes(self):
        """
        Asymmetric allocation of vCPU and Memory across the specific NUMA nodes (CPU sockets and memory banks).

        NOTE: symmetric numa_node_count should not be specified.
        """

Container.Architecture = _Architecture

@has_validated_properties
@dsl_specification('5.4.4', 'tosca-simple-profile-1.0')
class Endpoint(Root):
    """
    This is the default TOSCA type that should be used or extended to define a network endpoint capability. This includes the information to express a basic endpoint with a single port or a complex endpoint with multiple ports. By default the Endpoint is assumed to represent an address on a private network unless otherwise specified.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_CAPABILITIES_ENDPOINT>`__
    """

    SHORTHAND_NAME = 'Endpoint'
    TYPE_QUALIFIED_NAME = 'tosca:Endpoint'
    TYPE_URI = 'tosca.capabilities.Endpoint'

    @required_property
    @property_default('tcp')
    @property_type(str)
    @validated_property
    def protocol(self):
        """
        The name of the protocol (i.e., the protocol prefix) that the endpoint accepts (any OSI Layer 4-7 protocols). Examples: http, https, ftp, tcp, udp, etc.
        """

    @property_type(tosca.datatypes.network.PortDef)
    @validated_property
    def port(self):
        """
        The optional port of the endpoint.
        """

    @property_default(False)
    @property_type(bool)
    @validated_property
    def secure(self):
        """
        Requests for the endpoint to be secure and use credentials supplied on the ConnectsTo relationship.
        """

    @property_type(str)
    @validated_property
    def url_path(self):
        """
        The optional URL path of the endpoint\'s address if applicable for the protocol.
        """

    @property_type(str)
    @validated_property
    def port_name(self):
        """
        The optional name (or ID) of the network port this endpoint should be bound to.
        """

    @property_default('PRIVATE')
    @property_type(str)
    @validated_property
    def network_name(self):
        """
        The optional name (or ID) of the network this endpoint should be bound to. network_name: PRIVATE \| PUBLIC \| <network_name> \| <network_id>.
        """

    @property_default('source')
    @property_type(str)
    @validated_property
    def initiator(self):
        """
        The optional indicator of the direction of the connection.
        """

    @property_type(tosca.Map(tosca.datatypes.network.PortSpec))
    @validated_property
    def ports(self):
        """
        The optional map of ports the Endpoint supports (if more than one).
        """

    # Attributes

    @required_property
    @property_type(str)
    @validated_property
    def ip_address(self):
        """
        Note: This is the IP address as propagated up by the associated node's host (Compute) container.
        """
    
@has_validated_properties
@dsl_specification('5.4.5', 'tosca-simple-profile-1.0')
class _Public(Endpoint):
    """
    This capability represents a public endpoint which is accessible to the general internet (and its public IP address ranges).

    This public endpoint capability also can be used to create a floating (IP) address that the underlying network assigns from a pool allocated from the application's underlying public network. This floating address is managed by the underlying network such that can be routed an application's private address and remains reliable to internet clients.

    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_CAPABILITIES_ENDPOINT_PUBLIC>`__
    """
    
    SHORTHAND_NAME = 'Endpoint.Public'
    TYPE_QUALIFIED_NAME = 'tosca:Endpoint.Public'
    TYPE_URI = 'tosca.capabilities.Endpoint.Public'

    @property_default('PUBLIC')
    @property_type(str)
    @validated_property
    def network_name(self):
        """
        The optional name (or ID) of the network this endpoint should be bound to. network_name: PRIVATE \| PUBLIC \| <network_name> \| <network_id>.
        """

    @property_status('experimental')
    @property_default(False)
    @property_type(bool)
    @validated_property
    def floating(self):
        """
        Indicates that the public address should be allocated from a pool of floating IPs that are associated with the network.
        """

    @property_status('experimental')
    @property_type(str)
    @validated_property
    def dns_name(self):
        """
        The optional name to register with DNS.
        """

Endpoint.Public = _Public

@has_validated_properties
@dsl_specification('5.4.6', 'tosca-simple-profile-1.0')
class _Admin(Endpoint):
    """
    This is the default TOSCA type that should be used or extended to define a specialized administrator endpoint capability.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_CAPABILITIES_ENDPOINT_ADMIN>`__
    """
    
    SHORTHAND_NAME = 'Endpoint.Admin'
    TYPE_QUALIFIED_NAME = 'tosca:Endpoint.Admin'
    TYPE_URI = 'tosca.capabilities.Endpoint.Admin'

    @property_default(True)
    @property_type(bool)
    @validated_property
    def secure(self):
        """
        Requests for the endpoint to be secure and use credentials supplied on the ConnectsTo relationship.
        """

Endpoint.Admin = _Admin

@has_validated_properties
@dsl_specification('5.4.7', 'tosca-simple-profile-1.0')
class _Database(Endpoint):
    """
    This is the default TOSCA type that should be used or extended to define a specialized database endpoint capability.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_CAPABILITIES_ENDPOINT_DATABASE>`__
    """
    
    SHORTHAND_NAME = 'Endpoint.Database'
    TYPE_QUALIFIED_NAME = 'tosca:Endpoint.Database'
    TYPE_URI = 'tosca.capabilities.Endpoint.Database'

Endpoint.Database = _Database

@has_validated_properties
@dsl_specification('5.4.8', 'tosca-simple-profile-1.0')
class Attachment(Root):
    """
    This is the default TOSCA type that should be used or extended to define an attachment capability of a (logical) infrastructure device node (e.g., BlockStorage node).
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_CAPABILITIES_ATTACHMENT>`__
    """

    SHORTHAND_NAME = 'Attachment'
    TYPE_QUALIFIED_NAME = 'tosca:Attachment'
    TYPE_URI = 'tosca.capabilities.Attachment'

@has_validated_properties
@dsl_specification('5.4.9', 'tosca-simple-profile-1.0')
class OperatingSystem(Root):
    """
    This is the default TOSCA type that should be used to express an Operating System capability for a node.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_CAPABILITIES_OPSYS>`__
    """

    SHORTHAND_NAME = 'OperatingSystem'
    TYPE_QUALIFIED_NAME = 'tosca:OperatingSystem'
    TYPE_URI = 'tosca.capabilities.OperatingSystem'

    @property_type(str)
    @validated_property
    def architecture(self):
        """
        The Operating System (OS) architecture. Examples of valid values include: x86_32, x86_64, etc.
        """

    @property_type(str)
    @validated_property
    def type(self):
        """
        The Operating System (OS) type. Examples of valid values include: linux, aix, mac, windows, etc.
        """

    @property_type(str)
    @validated_property
    def distribution(self):
        """
        The Operating System (OS) distribution. Examples of valid values for a "type" of "Linux" would include:  debian, fedora, rhel and ubuntu.
        """

    @property_type(str)
    @validated_property
    def version(self):
        """
        The Operating System version.
        """

@has_validated_properties
@dsl_specification('5.4.10', 'tosca-simple-profile-1.0')
class Scalable(Root):
    """
    This is the default TOSCA type that should be used to express a scalability capability for a node.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_CAPABILITIES_SCALABLE>`__
    """

    SHORTHAND_NAME = 'Scalable'
    TYPE_QUALIFIED_NAME = 'tosca:Scalable'
    TYPE_URI = 'tosca.capabilities.Scalable'

    @required_property
    @property_default(1)
    @property_type(tosca.Integer)
    @validated_property
    def min_instances(self):
        """
        This property is used to indicate the minimum number of instances that should be created for the associated TOSCA Node Template by a TOSCA orchestrator.
        """

    @required_property
    @property_default(1)
    @property_type(tosca.Integer)
    @validated_property
    def max_instances(self):
        """
        This property is used to indicate the maximum number of instances that should be created for the associated TOSCA Node Template by a TOSCA orchestrator.
        """

    @property_type(tosca.Integer)
    @validated_property
    def default_instances(self):
        """
        An optional property that indicates the requested default number of instances that should be the starting number of instances a TOSCA orchestrator should attempt to allocate. Note: The value for this property MUST be in the range between the values set for "min_instances" and "max_instances" properties.
        """

MODULES = (
    'network',
    'nfv')

__all__ = (
    'MODULES',
    'Root',
    'Node',
    'Container',
    'Endpoint',
    'Attachment',
    'OperatingSystem',
    'Scalable')
