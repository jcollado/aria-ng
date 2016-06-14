
from aria import has_validated_properties, validated_property, property_type, property_default, required_property
import tosca, tosca.nodes, tosca.capabilities.network, tosca.capabilities.nfv

@has_validated_properties
class VNF(tosca.nodes.Root):
    """
    The NFV VNF Node Type represents a Virtual Network Function as defined by [ETSI GS NFV-MAN 001 v1.1.1]. It is the default type that all other VNF Node Types derive from. This allows for all VNF nodes to have a consistent set of features for modeling and management (e.g., consistent definitions for requirements, capabilities and lifecycle interfaces). 
    
    See the `TOSCA Simple Profile for NFV v1.0 specification <http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/tosca-nfv-v1.0.html#_Toc379455076>`__
    """

    SHORTHAND_NAME = 'VNF'
    TYPE_QUALIFIED_NAME = 'tosca:VNF'
    TYPE_URI = 'tosca.nodes.nfv.VNF'

    @property_type(str)
    @validated_property
    def id():
        """
        ID of this VNF.
        """

    @property_type(str)
    @validated_property
    def vendor():
        """
        Name of the vendor who generate this VNF.
        """

    @property_type(str)
    @validated_property
    def version():
        """
        Version of the software for this VNF.
        """

@has_validated_properties
class VDU(tosca.nodes.Root):
    """
    The NFV vdu node type represents a logical vdu entity as defined by [ETSI GS NFV-MAN 001 v1.1.1].
    
    See the `TOSCA Simple Profile for NFV v1.0 specification <http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/tosca-nfv-v1.0.html#_Toc419290242>`__
    """

    SHORTHAND_NAME = 'VDU'
    TYPE_QUALIFIED_NAME = 'tosca:VDU'
    TYPE_URI = 'tosca.nodes.nfv.VDU'
    
    # Capapilities

    @property_type(tosca.capabilities.nfv.Metric)
    @validated_property
    def monitoring_parameter():
        """
        Monitoring parameter, which can be tracked for a VNFC based on this VDU.

        Examples include: memory-consumption, CPU-utilisation, bandwidth-consumption, VNFC downtime, etc.
        """

    @property_type(tosca.capabilities.network.Bindable)
    @validated_property
    def virtualbinding():
        """
        Defines ability of VirtualBindable.
        """

@has_validated_properties
class CP(tosca.nodes.Root):
    """
    The NFV CP node represents a logical connection point entity as defined by [ETSI GS NFV-MAN 001 v1.1.1]. A connection point may be, for example, a virtual port, a virtual NIC address, a physical port, a physical NIC address or the endpoint of an IP VPN enabling network connectivity. It is assumed that each type of connection point will be modeled using subtypes of the CP type.
    
    See the `TOSCA Simple Profile for NFV v1.0 specification <http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/tosca-nfv-v1.0.html#_Toc419290245>`__
    """

    SHORTHAND_NAME = 'CP'
    TYPE_QUALIFIED_NAME = 'tosca:CP'
    TYPE_URI = 'tosca.nodes.nfv.CP'

    @property_type(str)
    @validated_property
    def type():
        """
        This may be, for example, a virtual port, a virtual NIC address, a SR-IOV port, a physical port, a physical NIC address or the endpoint of an IP VPN enabling network connectivity.
        """

    @property_type(str)
    @validated_property
    def anti_spoof_protection():
        """
        Indicates of whether anti-spoofing rule need to be enabled for this vNIC. This is applicable only when CP type is virtual NIC (vPort).
        """

    # Attributes
    
    @property_type(str)
    @validated_property
    def address():
        """
        The actual virtual NIC address that is been assigned when instantiating the connection point.
        """

@has_validated_properties
class VL(tosca.nodes.Root):
    """
    The NFV VL node type represents a logical virtual link entity as defined by [ETSI GS NFV-MAN 001 v1.1.1]. It is the default type from which all other virtual link types derive.
    
    See the `TOSCA Simple Profile for NFV v1.0 specification <http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/tosca-nfv-v1.0.html#_Toc419290251>`__
    """

    SHORTHAND_NAME = 'VL'
    TYPE_QUALIFIED_NAME = 'tosca:VL'
    TYPE_URI = 'tosca.nodes.nfv.VL'

    @property_type(str)
    @validated_property
    def vendor():
        """
        Vendor generating this VLD.
        """

@has_validated_properties
class ELine(VL):
    """
    The NFV VL.ELine node represents an E-Line virtual link entity.
    
    See the `TOSCA Simple Profile for NFV v1.0 specification <http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/tosca-nfv-v1.0.html#_Toc419290256>`__
    """

    SHORTHAND_NAME = 'VL.ELine'
    TYPE_QUALIFIED_NAME = 'tosca:ELine'
    TYPE_URI = 'tosca.nodes.nfv.VL.ELine'

VL.ELine = ELine

@has_validated_properties
class ELAN(VL):
    """
    The NFV VL.ELan node represents an E-LAN virtual link entity.
    
    See the `TOSCA Simple Profile for NFV v1.0 specification <http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/tosca-nfv-v1.0.html#_Toc419290257>`__
    """

    SHORTHAND_NAME = 'VL.ELAN'
    TYPE_QUALIFIED_NAME = 'tosca:ELAN'
    TYPE_URI = 'tosca.nodes.nfv.VL.ELAN'

VL.ELAN = ELAN

@has_validated_properties
class ETree(VL):
    """
    The NFV VL.ETree node represents an E-Tree virtual link entity.
    
    See the `TOSCA Simple Profile for NFV v1.0 specification <http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/tosca-nfv-v1.0.html#_Toc419290258>`__
    """

    SHORTHAND_NAME = 'VL.ETree'
    TYPE_QUALIFIED_NAME = 'tosca:ETree'
    TYPE_URI = 'tosca.nodes.nfv.VL.ETree'

VL.ETree = ETree

@has_validated_properties
class FP(VL):
    """
    The NFV FP node type represents a logical network forwarding path entity as defined by [ETSI GS NFV-MAN 001 v1.1.1].
    
    See the `TOSCA Simple Profile for NFV v1.0 specification <http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/tosca-nfv-v1.0.html#_Toc447714722>`__
    """

    SHORTHAND_NAME = 'FP'
    TYPE_QUALIFIED_NAME = 'tosca:FP'
    TYPE_URI = 'tosca.nodes.nfv.FP'

    @property_type(str)
    @validated_property
    def policy():
        """
        A policy or rule to apply to the NFP.
        """
