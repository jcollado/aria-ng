
from aria import dsl_specification, has_validated_properties, validated_property
import tosca, tosca.datatypes.network

@has_validated_properties
@dsl_specification('5.8.1', 'tosca-simple-profile-1.0')
class Root(object):
    """
    The TOSCA Root Node Type is the default type that all other TOSCA base Node Types derive from. This allows for all TOSCA nodes to have a consistent set of features for modeling and management (e.g., consistent definitions for requirements, capabilities and lifecycle interfaces).
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_NODES_ROOT>`__
    """

    SHORTHAND_NAME = 'Root'
    TYPE_QUALIFIED_NAME = 'tosca:Root'
    TYPE_URI = 'tosca.nodes.Root'

    # Attributes

    @validated_property(str, required=True)
    def tosca_id(self):
        """
        A unique identifier of the realized instance of a Node Template that derives from any TOSCA normative type.
        """

    @validated_property(str, required=True)
    def tosca_name(self):
        """
        This attribute reflects the name of the Node Template as defined in the TOSCA service template. This name is not unique to the realized instance model of corresponding deployed application as each template in the model can result in one or more instances (e.g., scaled) when orchestrated to a provider environment.
        """

    @validated_property(str, default='initial', required=True)
    def state(self):
        """
        The state of the node instance. See section "Node States" for allowed values.
        """

@has_validated_properties
@dsl_specification('5.8.2', 'tosca-simple-profile-1.0')
class Compute(Root):
    """
    The TOSCA Compute node represents one or more real or virtual processors of software applications or services along with other essential local resources. Collectively, the resources the compute node represents can logically be viewed as a (real or virtual) "server".
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_NODES_COMPUTE>`__
    """

    SHORTHAND_NAME = 'Compute'
    TYPE_QUALIFIED_NAME = 'tosca:Compute'
    TYPE_URI = 'tosca.nodes.Compute'

    # Attributes

    @validated_property(str)
    def private_address(self):
        """
        The primary private IP address assigned by the cloud provider that applications may use to access the Compute node.
        """

    @validated_property(str)
    def public_address(self):
        """
        The primary public IP address assigned by the cloud provider that applications may use to access the Compute node.
        """
        
    @validated_property(tosca.Map(tosca.datatypes.network.NetworkInfo))
    def networks(self):
        """
        The list of logical networks assigned to the compute host instance and information about them.
        """
        
    @validated_property(tosca.Map(tosca.datatypes.network.PortInfo))
    def ports(self):
        """
        The list of logical ports assigned to the compute host instance and information about them.
        """

@has_validated_properties
@dsl_specification('5.8.3', 'tosca-simple-profile-1.0')
class SoftwareComponent(Root):
    """
    The TOSCA SoftwareComponent node represents a generic software component that can be managed and run by a TOSCA Compute Node Type.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_NODES_SOFTWARE_COMPONENT>`__
    """

    SHORTHAND_NAME = 'SoftwareComponent'
    TYPE_QUALIFIED_NAME = 'tosca:SoftwareComponent'
    TYPE_URI = 'tosca.nodes.SoftwareComponent'

    @validated_property(tosca.Version)
    def component_version(self):
        """
        The optional software component's version.
        """

    @validated_property(tosca.datatypes.Credential)
    def admin_credential(self):
        """
        The optional credential that can be used to authenticate to the software component.
        """

@has_validated_properties
@dsl_specification('5.8.4', 'tosca-simple-profile-1.0')
class WebServer(SoftwareComponent):
    """
    This TOSA WebServer Node Type represents an abstract software component or service that is capable of hosting and providing management operations for one or more WebApplication nodes.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_NODES_WEBSERVER>`__
    """

    SHORTHAND_NAME = 'WebServer'
    TYPE_QUALIFIED_NAME = 'tosca:WebServer'
    TYPE_URI = 'tosca.nodes.WebServer'

@has_validated_properties
@dsl_specification('5.8.5', 'tosca-simple-profile-1.0')
class WebApplication(Root): # seems a mistake in spec: it should inherit SoftwareComponent, no?
    """
    The TOSCA WebApplication node represents a software application that can be managed and run by a TOSCA WebServer node. Specific types of web applications such as Java, etc. could be derived from this type.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_NODES_WEBAPPLICATION>`__
    """

    SHORTHAND_NAME = 'WebApplication'
    TYPE_QUALIFIED_NAME = 'tosca:WebApplication'
    TYPE_URI = 'tosca.nodes.WebApplication'

    @validated_property(str)
    def context_root(self):
        """
        The web application's context root which designates the application's URL path within the web server it is hosted on.
        """

@has_validated_properties
@dsl_specification('5.8.6', 'tosca-simple-profile-1.0')
class DBMS(SoftwareComponent):
    """
    The TOSCA DBMS node represents a typical relational, SQL Database Management System software component or service.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_NODES_WEBSERVER>`__
    """

    # Note: the names are missing from the spec
    SHORTHAND_NAME = 'DBMS'
    TYPE_QUALIFIED_NAME = 'tosca:DBMS'
    TYPE_URI = 'tosca.nodes.DMBS'

    @validated_property(str)
    def root_password(self):
        """
        The optional root password for the DBMS server.
        """

    @validated_property(tosca.Integer)
    def port(self):
        """
        The DBMS server's port.
        """

@has_validated_properties
@dsl_specification('5.8.7', 'tosca-simple-profile-1.0')
class Database(Root): # seems a mistake in spec: it should inherit SoftwareComponent, no?
    """
    The TOSCA Database node represents a logical database that can be managed and hosted by a TOSCA DBMS node.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_NODES_DATABASE>`__
    """

    SHORTHAND_NAME = 'Database'
    TYPE_QUALIFIED_NAME = 'tosca:Database'
    TYPE_URI = 'tosca.nodes.Database'

    @validated_property(str, required=True)
    def name(self):
        """
        The logical database Name.
        """

    @validated_property(tosca.Integer)
    def port(self):
        """
        The port the database service will use to listen for incoming data and requests.
        """

    @validated_property(str)
    def user(self):
        """
        The special user account used for database administration.
        """

    @validated_property(str)
    def password(self):
        """
        The password associated with the user account provided in the 'user' property.
        """

@has_validated_properties
@dsl_specification('5.8.8', 'tosca-simple-profile-1.0')
class ObjectStorage(Root):
    """
    The TOSCA ObjectStorage node represents storage that provides the ability to store data as objects (or BLOBs of data) without consideration for the underlying filesystem or devices.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#>`__ (no anchor)
    """

    SHORTHAND_NAME = 'ObjectStorage'
    TYPE_QUALIFIED_NAME = 'tosca:ObjectStorage'
    TYPE_URI = 'tosca.nodes.ObjectStorage'

    @validated_property(str, required=True)
    def name(self):
        """
        The logical name of the object store (or container).
        """

    @validated_property(tosca.Size)
    def size(self):
        """
        The requested initial storage size (default unit is in Gigabytes).
        """

    @validated_property(tosca.Size)
    def maxsize(self):
        """
        The requested maximum storage size (default unit is in Gigabytes).
        """

@has_validated_properties
@dsl_specification('5.8.9', 'tosca-simple-profile-1.0')
class BlockStorage(Root):
    """
    The TOSCA BlockStorage node currently represents a server-local block storage device (i.e., not shared) offering evenly sized blocks of data from which raw storage volumes can be created.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_NODES_BLOCK_STORAGE>`__
    """

    SHORTHAND_NAME = 'BlockStorage'
    TYPE_QUALIFIED_NAME = 'tosca:BlockStorage'
    TYPE_URI = 'tosca.nodes.BlockStorage'

    @validated_property(tosca.Size, required=True)
    def size(self):
        """
        The requested storage size (default unit is MB).
        """

    @validated_property(str)
    def volume_id(self):
        """
        ID of an existing volume (that is in the accessible scope of the requesting application).
        """

    @validated_property(str)
    def snapshot_id(self):
        """
        Some identifier that represents an existing snapshot that should be used when creating the block storage (volume).
        """

@has_validated_properties
class Container(object):
    pass
    
@has_validated_properties
@dsl_specification('5.8.10', 'tosca-simple-profile-1.0')
class _Runtime(SoftwareComponent):
    """
    The TOSCA Container Runtime node represents operating system-level virtualization technology used to run multiple application services on a single Compute host.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_NODES_CONTAINER_RUNTIME>`__
    """

    SHORTHAND_NAME = 'Container.Runtime'
    TYPE_QUALIFIED_NAME = 'tosca:Container.Runtime'
    TYPE_URI = 'tosca.nodes.Container.Runtime'

Container.Runtime = _Runtime

@has_validated_properties
@dsl_specification('5.8.11', 'tosca-simple-profile-1.0')
class _Application(Root):
    """
    The TOSCA Container Application node represents an application that requires Container-level virtualization technology.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_NODES_CONTAINER_APP>`__
    """

    SHORTHAND_NAME = 'Container.Application'
    TYPE_QUALIFIED_NAME = 'tosca:Container.Application'
    TYPE_URI = 'tosca.nodes.Container.Application'

Container.Application = _Application

@has_validated_properties
@dsl_specification('5.8.12', 'tosca-simple-profile-1.0')
class LoadBalancer(Root):
    """
    The TOSCA Load Balancer node represents logical function that be used in conjunction with a Floating Address to distribute an application's traffic (load) across a number of instances of the application (e.g., for a clustered or scaled application).
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc379548332>`__
    """

    SHORTHAND_NAME = 'LoadBalancer'
    TYPE_QUALIFIED_NAME = 'tosca:LoadBalancer'
    TYPE_URI = 'tosca.nodes.LoadBalancer'

MODULES = (
    'network',
    'nfv')

__all__ = (
    'MODULES',
    'Root',
    'Compute',
    'SoftwareComponent',
    'WebApplication',
    'Database',
    'ObjectStorage',
    'BlockStorage',
    'Container',
    'LoadBalancer')
