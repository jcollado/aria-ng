
from aria import dsl_specification, has_validated_properties, validated_property
import tosca.nodes

@has_validated_properties
@dsl_specification('7.5.1', 'tosca-simple-profile-1.0')
class Network(tosca.nodes.Root):
    """
    The TOSCA Network node represents a simple, logical network service.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#>`__ (no anchor)
    """

    SHORTHAND_NAME = 'Network'
    TYPE_QUALIFIED_NAME = 'tosca:Network'
    TYPE_URI = 'tosca.nodes.network.Network'

    @validated_property(tosca.Integer, default=5)
    def ip_version(self):
        """
        The IP version of the requested network.
        """

    @validated_property(str)
    def cidr(self):
        """
        The cidr block of the requested network.
        """

    @validated_property(str)
    def start_ip(self):
        """
        The IP address to be used as the 1st one in a pool of addresses derived from the cidr block full IP range.
        """

    @validated_property(str)
    def end_ip(self):
        """
        The IP address to be used as the last one in a pool of addresses derived from the cidr block full IP range.
        """

    @validated_property(str)
    def gateway_ip(self):
        """
        The gateway IP address.
        """

    @validated_property(str)
    def network_name(self):
        """
        An Identifier that represents an existing Network instance in the underlying cloud infrastructure - OR - be used as the name of the new created network.
        """

    @validated_property(str)
    def network_id(self):
        """
        An Identifier that represents an existing Network instance in the underlying cloud infrastructure. This property is mutually exclusive with all other properties except network_name.
        """

    @validated_property(str)
    def segmentation_id(self):
        """
        A segmentation identifier in the underlying cloud infrastructure (e.g., VLAN id, GRE tunnel id). If the segmentation_id is specified, the network_type or physical_network properties should be provided as well.
        """

    @validated_property(str)
    def network_type(self):
        """
        Optionally, specifies the nature of the physical network in the underlying cloud infrastructure. Examples are flat, vlan, gre or vxlan. For flat and vlan types, physical_network should be provided too.
        """

    @validated_property(str)
    def physical_network(self):
        """
        Optionally, identifies the physical network on top of which the network is implemented, e.g. physnet1. This property is required if network_type is flat or vlan.
        """

    @validated_property(bool, default=True)
    def dhcp_enabled(self):
        """
        Indicates the TOSCA container to create a virtual network instance with or without a DHCP service.
        """

@has_validated_properties
@dsl_specification('7.5.2', 'tosca-simple-profile-1.0')
class Port(tosca.nodes.Root):
    """
    The TOSCA Port node represents a logical entity that associates between Compute and Network normative types.
    
    The Port node type effectively represents a single virtual NIC on the Compute node instance.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#>`__ (no anchor)
    """

    SHORTHAND_NAME = 'Port'
    TYPE_QUALIFIED_NAME = 'tosca:Port'
    TYPE_URI = 'tosca.nodes.network.Port'

    @validated_property(str)
    def ip_address(self):
        """
        Allow the user to set a fixed IP address. Note that this address is a request to the provider which they will attempt to fulfill but may not be able to dependent on the network the port is associated with.
        """

    @validated_property(tosca.Integer, default=0)
    def order(self):
        """
        The order of the NIC on the compute instance (e.g. eth2). Note: when binding more than one port to a single compute (aka multi vNICs) and ordering is desired, it is *mandatory* that all ports will be set with an order value and. The order values must represent a positive, arithmetic progression that starts with 0 (e.g. 0, 1, 2, ..., n).
        """

    @validated_property(bool, default=False)
    def is_default(self):
        """
        Set is_default=true to apply a default gateway route on the running compute instance to the associated network gateway. Only one port that is associated to single compute node can set as default=true.
        """

    @validated_property(str)
    def ip_range_start(self):
        """
        Defines the starting IP of a range to be allocated for the compute instances that are associated by this Port. Without setting this property the IP allocation is done from the entire CIDR block of the network.
        """

    @validated_property(str)
    def ip_range_end(self):
        """
        Defines the ending IP of a range to be allocated for the compute instances that are associated by this Port. Without setting this property the IP allocation is done from the entire CIDR block of the network.
        """

__all__ = (
    'Network',
    'Port')
