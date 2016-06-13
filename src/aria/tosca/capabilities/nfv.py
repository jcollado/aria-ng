
from aria import has_validated_properties, validated_property, property_type, property_default, property_status, required_property
import tosca.capabilities

@has_validated_properties
class VirtualBindable(tosca.capabilities.Node):
    """
    A node type that includes the VirtualBindable capability indicates that it can be pointed by tosca.relationships.nfv.VirtualBindsTo relationship type.
    
    See the `TOSCA Simple Profile for NFV v1.0 specification <http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/tosca-nfv-v1.0.html#_Toc419290220>`__
    """

    SHORTHAND_NAME = 'VirtualBindable'
    TYPE_QUALIFIED_NAME = 'tosca:VirtualBindable'
    TYPE_URI = 'tosca.capabilities.nfv.VirtualBindable'

@has_validated_properties
class Metric(tosca.capabilities.Endpoint):
    """
    A node type that includes the Metric capability indicates that it can be monitored using an nfv.relationships.Monitor relationship type.
    
    See the `TOSCA Simple Profile for NFV v1.0 specification <http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/tosca-nfv-v1.0.html#_Toc418607874>`__
    """

    SHORTHAND_NAME = 'Metric'
    TYPE_QUALIFIED_NAME = 'tosca:Metric'
    TYPE_URI = 'tosca.capabilities.nfv.Metric'

@has_validated_properties
class Forwarder(tosca.capabilities.Root):
    """
    A node type that includes the Forwarder capability indicates that it can be pointed by tosca.relationships.nfv.FowardsTo relationship type.
    
    See the `TOSCA Simple Profile for NFV v1.0 specification <http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/tosca-nfv-v1.0.html#_Toc447714718>`__
    """

    SHORTHAND_NAME = 'Forwarder'
    TYPE_QUALIFIED_NAME = 'tosca:Forwarder'
    TYPE_URI = 'tosca.capabilities.nfv.Forwarder'

@has_validated_properties
class VirtualLinkable(tosca.capabilities.Node):
    """
    A node type that includes the VirtualLinkable capability indicates that it can be pointed by tosca.relationships.nfv.VirtualLinksTo relationship type.
    
    See the `TOSCA Simple Profile for NFV v1.0 specification <http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/tosca-nfv-v1.0.html#_Toc447714735>`__
    """

    SHORTHAND_NAME = 'VirtualLinkable'
    TYPE_QUALIFIED_NAME = 'tosca:VirtualLinkable'
    TYPE_URI = 'tosca.capabilities.nfv.VirtualLinkable'
