
import tosca, tosca.datatypes.network
	
class Root(tosca.HasProperties):
	"""
	The TOSCA Root Node Type is the default type that all other TOSCA base Node Types derive from. This allows for all TOSCA nodes to have a consistent set of features for modeling and management (e.g., consistent definitions for requirements, capabilities and lifecycle interfaces).
	
	See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_NODES_ROOT>`__
	"""
	
	DESCRIPTION = 'The TOSCA Root Node Type is the default type that all other TOSCA base Node Types derive from. This allows for all TOSCA nodes to have a consistent set of features for modeling and management (e.g., consistent definitions for requirements, capabilities and lifecycle interfaces).'

	SHORTHAND_NAME = 'Root'
	TYPE_QUALIFIED_NAME = 'tosca:Root'
	TYPE_URI = 'tosca.nodes.Root'

	ATTRIBUTES = {
		'tosca_id': {'type': str, 'required': True, 'description': 'A unique identifier of the realized instance of a Node Template that derives from any TOSCA normative type.'},
		'tosca_name': {'type': str, 'required': True, 'description': 'This attribute reflects the name of the Node Template as defined in the TOSCA service template. This name is not unique to the realized instance model of corresponding deployed application as each template in the model can result in one or more instances (e.g., scaled) when orchestrated to a provider environment.'},
		'state': {'type': str, 'required': True, 'default': 'initial', 'description': 'The state of the node instance. See section "Node States" for allowed values.'}}

class Compute(Root):
	"""
	The TOSCA Compute node represents one or more real or virtual processors of software applications or services along with other essential local resources. Collectively, the resources the compute node represents can logically be viewed as a (real or virtual) "server".
	
	See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_NODES_COMPUTE>`__
	"""
	
	DESCRIPTION = 'The TOSCA Compute node represents one or more real or virtual processors of software applications or services along with other essential local resources. Collectively, the resources the compute node represents can logically be viewed as a (real or virtual) "server".'

	SHORTHAND_NAME = 'Compute'
	TYPE_QUALIFIED_NAME = 'tosca:Compute'
	TYPE_URI = 'tosca.nodes.Compute'

	ATTRIBUTES = {
		'private_address': {'type': str, 'description': 'The primary private IP address assigned by the cloud provider that applications may use to access the Compute node.'},
		'public_address': {'type': str, 'description': 'The primary public IP address assigned by the cloud provider that applications may use to access the Compute node.'},
		'networks': {'type': tosca.Map(tosca.datatypes.network.NetworkInfo), 'description': 'The list of logical networks assigned to the compute host instance and information about them.'},
		'ports': {'type': tosca.Map(tosca.datatypes.network.PortInfo), 'description': 'The list of logical ports assigned to the compute host instance and information about them.'}}

class SoftwareComponent(Root):
	"""
	The TOSCA SoftwareComponent node represents a generic software component that can be managed and run by a TOSCA Compute Node Type.
	
	See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_NODES_SOFTWARE_COMPONENT>`__
	"""
	
	DESCRIPTION = 'The TOSCA SoftwareComponent node represents a generic software component that can be managed and run by a TOSCA Compute Node Type.'

	SHORTHAND_NAME = 'SoftwareComponent'
	TYPE_QUALIFIED_NAME = 'tosca:SoftwareComponent'
	TYPE_URI = 'tosca.nodes.SoftwareComponent'
	
	PROPERTIES = {
		'component_version': {'type': tosca.Version, 'description': 'The optional software component\'s version.'},
		'admin_credential': {'type': tosca.datatypes.Credential, 'description': 'The optional credential that can be used to authenticate to the software component.'}}

class WebServer(SoftwareComponent):
	"""
	This TOSA WebServer Node Type represents an abstract software component or service that is capable of hosting and providing management operations for one or more WebApplication nodes.
	
	See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_NODES_WEBSERVER>`__
	"""
	
	DESCRIPTION = 'This TOSA WebServer Node Type represents an abstract software component or service that is capable of hosting and providing management operations for one or more WebApplication nodes.'

	SHORTHAND_NAME = 'WebServer'
	TYPE_QUALIFIED_NAME = 'tosca:WebServer'
	TYPE_URI = 'tosca.nodes.WebServer'

class WebApplication(Root):
	"""
	The TOSCA WebApplication node represents a software application that can be managed and run by a TOSCA WebServer node. Specific types of web applications such as Java, etc. could be derived from this type.
	
	See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_NODES_WEBAPPLICATION>`__
	"""
	
	DESCRIPTION = 'The TOSCA WebApplication node represents a software application that can be managed and run by a TOSCA WebServer node. Specific types of web applications such as Java, etc. could be derived from this type.'

	SHORTHAND_NAME = 'WebApplication'
	TYPE_QUALIFIED_NAME = 'tosca:WebApplication'
	TYPE_URI = 'tosca.nodes.WebApplication'

	PROPERTIES = {
		'context_root': {'type': str, 'description': 'The web application\'s context root which designates the application\'s URL path within the web server it is hosted on.'}}

class DBMS(SoftwareComponent):
	"""
	The TOSCA DBMS node represents a typical relational, SQL Database Management System software component or service.
	
	See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_NODES_WEBSERVER>`__
	"""
	
	DESCRIPTION = 'The TOSCA DBMS node represents a typical relational, SQL Database Management System software component or service.'

	# Note: the names are missing from the spec
	SHORTHAND_NAME = 'DBMS'
	TYPE_QUALIFIED_NAME = 'tosca:DBMS'
	TYPE_URI = 'tosca.nodes.DMBS'

	PROPERTIES = {
		'root_password': {'type': str, 'description': 'The optional root password for the DBMS server.'},
		'port': {'type': tosca.Integer, 'description': 'The DBMS server\'s port.'}}

class Database(Root):
	"""
	The TOSCA Database node represents a logical database that can be managed and hosted by a TOSCA DBMS node.
	
	See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_NODES_DATABASE>`__
	"""
	
	DESCRIPTION = 'The TOSCA Database node represents a logical database that can be managed and hosted by a TOSCA DBMS node.'

	SHORTHAND_NAME = 'Database'
	TYPE_QUALIFIED_NAME = 'tosca:Database'
	TYPE_URI = 'tosca.nodes.Database'

	PROPERTIES = {
		'name': {'type': str, 'required': True, 'description': 'The logical database Name.'},
		'port': {'type': tosca.Integer, 'description': 'The port the database service will use to listen for incoming data and requests.'},
		'user': {'type': str, 'description': 'The special user account used for database administration.'},
		'password': {'type': str, 'description': 'The password associated with the user account provided in the \'user\' property.'}}

class ObjectStorage(Root):
	"""
	The TOSCA ObjectStorage node represents storage that provides the ability to store data as objects (or BLOBs of data) without consideration for the underlying filesystem or devices.
	
	See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#>`__ (no anchor)
	"""
	
	DESCRIPTION = 'The TOSCA ObjectStorage node represents storage that provides the ability to store data as objects (or BLOBs of data) without consideration for the underlying filesystem or devices.'

	SHORTHAND_NAME = 'ObjectStorage'
	TYPE_QUALIFIED_NAME = 'tosca:ObjectStorage'
	TYPE_URI = 'tosca.nodes.ObjectStorage'

	PROPERTIES = {
		'name': {'type': str, 'required': True, 'description': 'The logical name of the object store (or container).'},
		'size': {'type': tosca.Size, 'description': 'The requested initial storage size (default unit is in Gigabytes).'},
		'maxsize': {'type': tosca.Size, 'description': 'The requested maximum storage size (default unit is in Gigabytes).'}}

class BlockStorage(Root):
    """
    The TOSCA BlockStorage node currently represents a server-local block storage device (i.e., not shared) offering evenly sized blocks of data from which raw storage volumes can be created.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_NODES_BLOCK_STORAGE>`__
    """
    
    DESCRIPTION = 'The TOSCA BlockStorage node currently represents a server-local block storage device (i.e., not shared) offering evenly sized blocks of data from which raw storage volumes can be created.'

    SHORTHAND_NAME = 'BlockStorage'
    TYPE_QUALIFIED_NAME = 'tosca:BlockStorage'
    TYPE_URI = 'tosca.nodes.BlockStorage'

    PROPERTIES = {
        'size': {'type': tosca.Size, 'required': True, 'description': 'The requested storage size (default unit is MB).'},
        'volume_id': {'type': str, 'description': 'ID of an existing volume (that is in the accessible scope of the requesting application).'},
        'snapshot_id': {'type': str, 'description': 'Some identifier that represents an existing snapshot that should be used when creating the block storage (volume).'}}

class Container(object):
    pass
	
class Runtime(SoftwareComponent):
    """
    The TOSCA Container Runtime node represents operating system-level virtualization technology used to run multiple application services on a single Compute host.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_NODES_CONTAINER_RUNTIME>`__
    """
    
    DESCRIPTION = 'The TOSCA Container Runtime node represents operating system-level virtualization technology used to run multiple application services on a single Compute host.'

    SHORTHAND_NAME = 'Container.Runtime'
    TYPE_QUALIFIED_NAME = 'tosca:Container.Runtime'
    TYPE_URI = 'tosca.nodes.Container.Runtime'

Container.Runtime = Runtime

class Application(Root):
    """
    The TOSCA Container Application node represents an application that requires Container-level virtualization technology.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_NODES_CONTAINER_APP>`__
    """
    
    DESCRIPTION = 'The TOSCA Container Application node represents an application that requires Container-level virtualization technology.'

    SHORTHAND_NAME = 'Container.Application'
    TYPE_QUALIFIED_NAME = 'tosca:Container.Application'
    TYPE_URI = 'tosca.nodes.Container.Application'

Container.Application = Application

class LoadBalancer(Root):
	"""
	The TOSCA Load Balancer node represents logical function that be used in conjunction with a Floating Address to distribute an application's traffic (load) across a number of instances of the application (e.g., for a clustered or scaled application).
	
	See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc379548332>`__
	"""
	
	DESCRIPTION = 'The TOSCA Load Balancer node represents logical function that be used in conjunction with a Floating Address to distribute an application\'s traffic (load) across a number of instances of the application (e.g., for a clustered or scaled application).'

	SHORTHAND_NAME = 'LoadBalancer'
	TYPE_QUALIFIED_NAME = 'tosca:LoadBalancer'
	TYPE_URI = 'tosca.nodes.LoadBalancer'
