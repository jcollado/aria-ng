
from aria import tosca_specification, has_validated_properties, validated_property, property_type, property_default, required_property
import tosca, tosca.nodes

@has_validated_properties
@tosca_specification('7.5.1')
class Network(tosca.nodes.Root):
    """
    The TOSCA Network node represents a simple, logical network service.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#>`__ (no anchor)
    """

    SHORTHAND_NAME = 'Network'
    TYPE_QUALIFIED_NAME = 'tosca:Network'
    TYPE_URI = 'tosca.nodes.network.Network'

    @property_default(4)
    @property_type(tosca.Integer)
    @validated_property
    def ip_version():
        """
        The IP version of the requested network.
        """

    @property_type(str)
    @validated_property
    def cidr():
        """
        The cidr block of the requested network.
        """

    @property_type(str)
    @validated_property
    def start_ip():
        """
        The IP address to be used as the 1st one in a pool of addresses derived from the cidr block full IP range.
        """

    @property_type(str)
    @validated_property
    def end_ip():
        """
        The IP address to be used as the last one in a pool of addresses derived from the cidr block full IP range.
        """

    @property_type(str)
    @validated_property
    def gateway_ip():
        """
        The gateway IP address.
        """

    @property_type(str)
    @validated_property
    def network_name():
        """
        An Identifier that represents an existing Network instance in the underlying cloud infrastructure - OR - be used as the name of the new created network.
        """

    @property_type(str)
    @validated_property
    def network_id():
        """
        An Identifier that represents an existing Network instance in the underlying cloud infrastructure. This property is mutually exclusive with all other properties except network_name.
        """

    @property_type(str)
    @validated_property
    def segmentation_id():
        """
        A segmentation identifier in the underlying cloud infrastructure (e.g., VLAN id, GRE tunnel id). If the segmentation_id is specified, the network_type or physical_network properties should be provided as well.
        """

    @property_type(str)
    @validated_property
    def network_type():
        """
        Optionally, specifies the nature of the physical network in the underlying cloud infrastructure. Examples are flat, vlan, gre or vxlan. For flat and vlan types, physical_network should be provided too.
        """

    @property_type(str)
    @validated_property
    def physical_network():
        """
        Optionally, identifies the physical network on top of which the network is implemented, e.g. physnet1. This property is required if network_type is flat or vlan.
        """

    @property_default(True)
    @property_type(bool)
    @validated_property
    def dhcp_enabled():
        """
        Indicates the TOSCA container to create a virtual network instance with or without a DHCP service.
        """

@has_validated_properties
@tosca_specification('7.5.2')
class Port(tosca.nodes.Root):
    """
    The TOSCA Port node represents a logical entity that associates between Compute and Network normative types.
    
    The Port node type effectively represents a single virtual NIC on the Compute node instance.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#>`__ (no anchor)
    """

    SHORTHAND_NAME = 'Port'
    TYPE_QUALIFIED_NAME = 'tosca:Port'
    TYPE_URI = 'tosca.nodes.network.Port'

    @property_type(str)
    @validated_property
    def ip_address():
        """
        Allow the user to set a fixed IP address. Note that this address is a request to the provider which they will attempt to fulfill but may not be able to dependent on the network the port is associated with.
        """

    @property_default(0)
    @property_type(tosca.Integer)
    @validated_property
    def order():
        """
        The order of the NIC on the compute instance (e.g. eth2). Note: when binding more than one port to a single compute (aka multi vNICs) and ordering is desired, it is *mandatory* that all ports will be set with an order value and. The order values must represent a positive, arithmetic progression that starts with 0 (e.g. 0, 1, 2, ..., n).
        """

    @property_default(False)
    @property_type(bool)
    @validated_property
    def is_default():
        """
        Set is_default=true to apply a default gateway route on the running compute instance to the associated network gateway. Only one port that is associated to single compute node can set as default=true.
        """

    @property_type(str)
    @validated_property
    def ip_range_start():
        """
        Defines the starting IP of a range to be allocated for the compute instances that are associated by this Port. Without setting this property the IP allocation is done from the entire CIDR block of the network.
        """

    @property_type(str)
    @validated_property
    def ip_range_end():
        """
        Defines the ending IP of a range to be allocated for the compute instances that are associated by this Port. Without setting this property the IP allocation is done from the entire CIDR block of the network.
        """
