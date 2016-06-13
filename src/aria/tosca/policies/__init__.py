
from aria import has_validated_properties, validated_property, property_type, property_default, required_property
import tosca
    
@has_validated_properties
class Root(object):
    """
    This is the default (root) TOSCA Policy Type definition that is used to govern placement of TOSCA nodes or groups of nodes.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_POLICIES_ROOT>`__
    """

@has_validated_properties
class Placement(Root):
    """
    This is the default (root) TOSCA Policy Type definition that is used to govern placement of TOSCA nodes or groups of nodes.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_POLICIES_PLACEMENT>`__
    """

@has_validated_properties
class Scaling(Root):
    """
    This is the default (root) TOSCA Policy Type definition that is used to govern scaling of TOSCA nodes or groups of nodes.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_POLICIES_SCALING>`__
    """

@has_validated_properties
class Update(Root):
    """
    This is the default (root) TOSCA Policy Type definition that is used to govern update of TOSCA nodes or groups of nodes.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_POLICIES_UPDATE>`__
    """

@has_validated_properties
class Performance(Root):
    """
    This is the default (root) TOSCA Policy Type definition that is used to declare performance requirements for TOSCA nodes or groups of nodes.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_POLICIES_PERFORMANCE>`__
    """
