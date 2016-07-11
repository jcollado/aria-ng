
from aria import dsl_specification, has_validated_properties
import tosca
    
@has_validated_properties
@dsl_specification('5.10.1', 'tosca-simple-profile-1.0')
class Root(object):
    """
    This is the default (root) TOSCA Policy Type definition that is used to govern placement of TOSCA nodes or groups of nodes.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_POLICIES_ROOT>`__
    """

@has_validated_properties
@dsl_specification('5.10.2', 'tosca-simple-profile-1.0')
class Placement(Root):
    """
    This is the default (root) TOSCA Policy Type definition that is used to govern placement of TOSCA nodes or groups of nodes.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_POLICIES_PLACEMENT>`__
    """

@has_validated_properties
@dsl_specification('5.10.3', 'tosca-simple-profile-1.0')
class Scaling(Root):
    """
    This is the default (root) TOSCA Policy Type definition that is used to govern scaling of TOSCA nodes or groups of nodes.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_POLICIES_SCALING>`__
    """

@has_validated_properties
@dsl_specification('5.10.4', 'tosca-simple-profile-1.0')
class Update(Root):
    """
    This is the default (root) TOSCA Policy Type definition that is used to govern update of TOSCA nodes or groups of nodes.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_POLICIES_UPDATE>`__
    """

@has_validated_properties
@dsl_specification('5.10.5', 'tosca-simple-profile-1.0')
class Performance(Root):
    """
    This is the default (root) TOSCA Policy Type definition that is used to declare performance requirements for TOSCA nodes or groups of nodes.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_POLICIES_PERFORMANCE>`__
    """

__all__ = (
    'Root',
    'Placement',
    'Scaling',
    'Update',
    'Performance')
