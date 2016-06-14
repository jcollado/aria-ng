
from aria import tosca_specification, has_validated_properties, validated_property, property_type, property_default, property_status, required_property
import tosca, tosca.capabilities
    
@has_validated_properties
@tosca_specification('5.4.11')
class Bindable(tosca.capabilities.Node):
    """
    A node type that includes the Bindable capability indicates that it can be bound to a logical network association via a network port.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_CAPABILITIES_NETWORK_BINDABLE>`__
    """

    SHORTHAND_NAME = 'network.Bindable'
    TYPE_QUALIFIED_NAME = 'tosca:network.Bindable'
    TYPE_URI = 'tosca.capabilities.network.Bindable'

@has_validated_properties
@tosca_specification('7.5.3')
class Linkable(tosca.capabilities.Node):
    """
    A node type that includes the Linkable capability indicates that it can be pointed by tosca.relationships.network.LinksTo relationship type.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_CAPABILITIES_NETWORK_LINKABLE>`__
    """

    # Note: different style from Bindable :/
    SHORTHAND_NAME = 'Linkable'
    TYPE_QUALIFIED_NAME = 'tosca:Linkable'
    TYPE_URI = 'tosca.capabilities.network.Linkable'
