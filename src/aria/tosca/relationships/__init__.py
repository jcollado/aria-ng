
from aria import has_validated_properties, validated_property, property_type, property_default, required_property
import tosca, tosca.datatypes
    
class Root(tosca.HasProperties):
    """
    This is the default (root) TOSCA Relationship Type definition that all other TOSCA Relationship Types derive from.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_RELATIONSHIPS_ROOT>`__
    """
    
    DESCRIPTION = 'This is the default (root) TOSCA Relationship Type definition that all other TOSCA Relationship Types derive from.'

    ATTRIBUTES = {
        'tosca_id': {'type': str, 'required': True, 'description': 'A unique identifier of the realized instance of a Relationship Template that derives from any TOSCA normative type.'},
        'tosca_name': {'type': str, 'required': True, 'description': 'This attribute reflects the name of the Relationship Template as defined in the TOSCA service template. This name is not unique to the realized instance model of corresponding deployed application as each template in the model can result in one or more instances (e.g., scaled) when orchestrated to a provider environment.'},
        'state': {'type': str, 'required': True, 'default': 'initial', 'description': 'The state of the relationship instance. See section "Relationship States" for allowed values.'}}

class DependsOn(Root):
    """
    This type represents a general dependency relationship between two nodes.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_RELATIONSHIPS_DEPENDSON>`__
    """
    
    DESCRIPTION = 'This type represents a general dependency relationship between two nodes.'

    SHORTHAND_NAME = 'DependsOn'
    TYPE_QUALIFIED_NAME = 'tosca:DependsOn'
    TYPE_URI = 'tosca.relationships.DependsOn'

class HostedOn(Root):
    """
    This type represents a hosting relationship between two nodes.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_RELATIONSHIPS_HOSTEDON>`__
    """
    
    DESCRIPTION = 'This type represents a hosting relationship between two nodes.'

    SHORTHAND_NAME = 'HostedOn'
    TYPE_QUALIFIED_NAME = 'tosca:HostedOn'
    TYPE_URI = 'tosca.relationships.HostedOn'

@has_validated_properties
class ConnectsTo(Root):
    """
    This type represents a network connection relationship between two nodes.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_RELATIONSHIPS_CONNECTSTO>`__
    """
    
    DESCRIPTION = 'This type represents a network connection relationship between two nodes.'

    SHORTHAND_NAME = 'ConnectsTo'
    TYPE_QUALIFIED_NAME = 'tosca:ConnectsTo'
    TYPE_URI = 'tosca.relationships.ConnectsTo'

    @property_type(tosca.datatypes.Credential)
    @validated_property
    def credential(self):
        """
        The security credential to use to present to the target endpoint to for either authentication or authorization purposes.
        """

@has_validated_properties
class AttachesTo(Root):
    """
    This type represents an attachment relationship between two nodes. For example, an AttachesTo relationship type would be used for attaching a storage node to a Compute node.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_RELATIONSHIPS_ATTACHTO>`__
    """
    
    DESCRIPTION = 'This type represents an attachment relationship between two nodes. For example, an AttachesTo relationship type would be used for attaching a storage node to a Compute node.'

    SHORTHAND_NAME = 'AttachesTo'
    TYPE_QUALIFIED_NAME = 'tosca:AttachesTo'
    TYPE_URI = 'tosca.relationships.AttachesTo'

    @required_property
    @property_type(str)
    @validated_property
    def location(self):
        """
        The relative location (e.g., path on the file system), which provides the root location to address an attached node. e.g., a mount point / path such as '/usr/data'. Note: The user must provide it and it cannot be "root".
        """

    @property_type(str)
    @validated_property
    def device(self):
        """
        The logical device name which for the attached device (which is represented by the target node in the model). e.g., '/dev/hda1'.
        """
    
    ATTRIBUTES = {
        'device': {'type': str, 'description': 'The logical name of the device as exposed to the instance. Note: A runtime property that gets set when the model gets instantiated by the orchestrator.'}}

class RoutesTo(ConnectsTo):
    """
    This type represents an intentional network routing between two Endpoints in different networks.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc397688815>`__
    """
    
    DESCRIPTION = 'This type represents an intentional network routing between two Endpoints in different networks.'

    SHORTHAND_NAME = 'RoutesTo'
    TYPE_QUALIFIED_NAME = 'tosca:RoutesTo'
    TYPE_URI = 'tosca.relationships.RoutesTo'
