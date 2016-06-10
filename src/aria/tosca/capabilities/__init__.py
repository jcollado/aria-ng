
import tosca
    
class Root(tosca.HasProperties):
    """
    This is the default (root) TOSCA Capability Type definition that all other TOSCA Capability Types derive from.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_CAPABILITIES_ROOT>`
    """
    
    DESCRIPTION = 'This is the default (root) TOSCA Capability Type definition that all other TOSCA Capability Types derive from.'

class Node(Root):
    """
    The Node capability indicates the base capabilities of a TOSCA Node Type.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_CAPABILITIES_NODE>`
    """
    
    DESCRIPTION = 'The Node capability indicates the base capabilities of a TOSCA Node Type.'

    SHORTHAND_NAME = 'Node'
    TYPE_QUALIFIED_NAME = 'tosca:Node'
    TYPE_URI = 'tosca.capabilities.Node'

class Container(Root):
    """
    The Container capability, when included on a Node Type or Template definition, indicates that the node can act as a container for (or a host for) one or more other declared Node Types.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_CAPABILITIES_CONTAINER>`
    """
    
    DESCRIPTION = 'The Container capability, when included on a Node Type or Template definition, indicates that the node can act as a container for (or a host for) one or more other declared Node Types.'

    SHORTHAND_NAME = 'Container'
    TYPE_QUALIFIED_NAME = 'tosca:Container'
    TYPE_URI = 'tosca.capabilities.Container'

    PROPERTIES = {
        'num_cpus': {'type': tosca.Integer, 'description': 'Number of (actual or virtual) CPUs associated with the Compute node.'},
        'cpu_frequency': {'type': tosca.Frequency, 'description': 'Specifies the operating frequency of CPU\'s core. This property expresses the expected frequency of one (1) CPU as provided by the property "num_cpus".'},
        'disk_size': {'type': tosca.Size, 'description': 'Size of the local disk available to applications running on the Compute node (default unit is MB).'},
        'mem_size': {'type': tosca.Size, 'description': 'Size of memory available to applications running on the Compute node (default unit is MB).'}}

class Endpoint(Root):
    """
    This is the default TOSCA type that should be used or extended to define a network endpoint capability. This includes the information to express a basic endpoint with a single port or a complex endpoint with multiple ports. By default the Endpoint is assumed to represent an address on a private network unless otherwise specified.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_CAPABILITIES_ENDPOINT>`
    """
    
    DESCRIPTION = 'This is the default TOSCA type that should be used or extended to define a network endpoint capability. This includes the information to express a basic endpoint with a single port or a complex endpoint with multiple ports. By default the Endpoint is assumed to represent an address on a private network unless otherwise specified.'

    SHORTHAND_NAME = 'Endpoint'
    TYPE_QUALIFIED_NAME = 'tosca:Endpoint'
    TYPE_URI = 'tosca.capabilities.Endpoint'

    PROPERTIES = {
        'protocol': {'type': str, 'required': True, 'default': 'tcp', 'description': 'The name of the protocol (i.e., the protocol prefix) that the endpoint accepts (any OSI Layer 4-7 protocols). Examples: http, https, ftp, tcp, udp, etc.'},
        'port': {'type': tosca.datatypes.network.PortDef, 'description': 'The optional port of the endpoint.'},
        'secure': {'type': bool, 'default': False, 'description': 'Requests for the endpoint to be secure and use credentials supplied on the ConnectsTo relationship.'},
        'url_path': {'type': str, 'description': 'The optional URL path of the endpoint's address if applicable for the protocol.'},
        'port_name': {'type': str, 'description': 'The optional name (or ID) of the network port this endpoint should be bound to.'},
        'network_name': {'type': str, 'default': 'PRIVATE', 'description': 'The optional name (or ID) of the network this endpoint should be bound to. network_name: PRIVATE | PUBLIC |<network_name> | <network_id>'},
        'initiator': {'type': str, 'default': 'source', 'description': 'The optional indicator of the direction of the connection.'},
        'ports': {'type': tosca.Map(tosca.datatypes.network.PortSpec), 'description': 'The optional map of ports the Endpoint supports (if more than one)'}}

    ATTRIBUTES = {
        'ip_address': {'type': str, 'required': True, 'description': 'Note: This is the IP address as propagated up by the associated node's host (Compute) container.'}}
    
    class Public(Endpoint):
        """
        This capability represents a public endpoint which is accessible to the general internet (and its public IP address ranges).

        This public endpoint capability also can be used to create a floating (IP) address that the underlying network assigns from a pool allocated from the application's underlying public network. This floating address is managed by the underlying network such that can be routed an application's private address and remains reliable to internet clients.

        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_CAPABILITIES_ENDPOINT_PUBLIC>`
        """
        
        DESCRIPTION = 'This capability represents a public endpoint which is accessible to the general internet (and its public IP address ranges).'
        
        SHORTHAND_NAME = 'Endpoint.Public'
        TYPE_QUALIFIED_NAME = 'tosca:Endpoint.Public'
        TYPE_URI = 'tosca.capabilities.Endpoint.Public'

        PROPERTIES = {
            'network_name': {'type': str, 'default': 'PUBLIC', 'description': 'The optional name (or ID) of the network this endpoint should be bound to. network_name: PRIVATE | PUBLIC |<network_name> | <network_id>'},
            'floating': {'type': bool, 'default': False, 'description': 'Indicates that the public address should be allocated from a pool of floating IPs that are associated with the network.', 'status': 'experimental'},
            'dns_name': {'type': str, 'description': 'The optional name to register with DNS.', 'status': 'experimental'}}

    class Admin(Endpoint):
        """
        This is the default TOSCA type that should be used or extended to define a specialized administrator endpoint capability.
        
        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_CAPABILITIES_ENDPOINT_ADMIN>`
        """
        
        DESCRIPTION = 'This is the default TOSCA type that should be used or extended to define a specialized administrator endpoint capability.'
        
        SHORTHAND_NAME = 'Endpoint.Admin'
        TYPE_QUALIFIED_NAME = 'tosca:Endpoint.Admin'
        TYPE_URI = 'tosca.capabilities.Endpoint.Admin'

        PROPERTIES = {
            'secure': {'type': bool, 'default': True, 'description': 'Requests for the endpoint to be secure and use credentials supplied on the ConnectsTo relationship.'}}

    class Database(Endpoint):
        """
        This is the default TOSCA type that should be used or extended to define a specialized database endpoint capability.
        
        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_CAPABILITIES_ENDPOINT_DATABASE>`
        """
        
        DESCRIPTION = 'This is the default TOSCA type that should be used or extended to define a specialized database endpoint capability.'
        
        SHORTHAND_NAME = 'Endpoint.Database'
        TYPE_QUALIFIED_NAME = 'tosca:Endpoint.Database'
        TYPE_URI = 'tosca.capabilities.Endpoint.Database'

class Attachment(Root):
    """
    This is the default TOSCA type that should be used or extended to define an attachment capability of a (logical) infrastructure device node (e.g., BlockStorage node).
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_CAPABILITIES_ATTACHMENT>`
    """
    
    DESCRIPTION = 'This is the default TOSCA type that should be used or extended to define an attachment capability of a (logical) infrastructure device node (e.g., BlockStorage node).'

    SHORTHAND_NAME = 'Attachment'
    TYPE_QUALIFIED_NAME = 'tosca:Attachment'
    TYPE_URI = 'tosca.capabilities.Attachment'

class OperatingSystem(Root):
    """
    This is the default TOSCA type that should be used to express an Operating System capability for a node.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_CAPABILITIES_OPSYS>`
    """
    
    DESCRIPTION = 'This is the default TOSCA type that should be used to express an Operating System capability for a node.'

    SHORTHAND_NAME = 'OperatingSystem'
    TYPE_QUALIFIED_NAME = 'tosca:OperatingSystem'
    TYPE_URI = 'tosca.capabilities.OperatingSystem'

    PROPERTIES = {
        'architecture': {'type': str, 'description': 'The Operating System (OS) architecture. Examples of valid values include: x86_32, x86_64, etc.'},
        'type': {'type': str, 'description': 'The Operating System (OS) type. Examples of valid values include: linux, aix, mac, windows, etc.'},
        'distribution': {'type': str, 'description': 'The Operating System (OS) distribution. Examples of valid values for a "type" of "Linux" would include:  debian, fedora, rhel and ubuntu.'},
        'version': {'type': str, 'description': 'The Operating System version.'}}

class Scalable(Root):
    """
    This is the default TOSCA type that should be used to express a scalability capability for a node.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_CAPABILITIES_SCALABLE>`
    """
    
    DESCRIPTION = 'This is the default TOSCA type that should be used to express a scalability capability for a node.'

    SHORTHAND_NAME = 'Scalable'
    TYPE_QUALIFIED_NAME = 'tosca:Scalable'
    TYPE_URI = 'tosca.capabilities.Scalable'

    PROPERTIES = {
        'min_instances': {'type': tosca.Integer, 'required': True, 'default': 1, 'description': 'This property is used to indicate the minimum number of instances that should be created for the associated TOSCA Node Template by a TOSCA orchestrator.'},
        'max_instances': {'type': tosca.Integer, 'required': True, 'default': 1, 'description': 'This property is used to indicate the maximum number of instances that should be created for the associated TOSCA Node Template by a TOSCA orchestrator.'},
        'default_instances': {'type': tosca.Integer, 'description': 'An optional property that indicates the requested default number of instances that should be the starting number of instances a TOSCA orchestrator should attempt to allocate. Note: The value for this property MUST be in the range between the values set for "min_instances" and "max_instances" properties.'}}
