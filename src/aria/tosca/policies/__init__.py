
import tosca
    
class Root(tosca.HasProperties):
    """
    This is the default (root) TOSCA Policy Type definition that is used to govern placement of TOSCA nodes or groups of nodes.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_POLICIES_ROOT>`
    """
    
    DESCRIPTION = 'This is the default (root) TOSCA Policy Type definition that is used to govern placement of TOSCA nodes or groups of nodes.'

class Placement(Root):
    """
    This is the default (root) TOSCA Policy Type definition that is used to govern placement of TOSCA nodes or groups of nodes.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_POLICIES_PLACEMENT>`
    """
    
    DESCRIPTION = 'This is the default (root) TOSCA Policy Type definition that is used to govern placement of TOSCA nodes or groups of nodes.'

class Scaling(Root):
    """
    This is the default (root) TOSCA Policy Type definition that is used to govern scaling of TOSCA nodes or groups of nodes.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_POLICIES_SCALING>`
    """
    
    DESCRIPTION = 'This is the default (root) TOSCA Policy Type definition that is used to govern scaling of TOSCA nodes or groups of nodes.'

class Update(Root):
    """
    This is the default (root) TOSCA Policy Type definition that is used to govern update of TOSCA nodes or groups of nodes.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_POLICIES_UPDATE>`
    """
    
    DESCRIPTION = 'This is the default (root) TOSCA Policy Type definition that is used to govern update of TOSCA nodes or groups of nodes.'

class Performance(Root):
    """
    This is the default (root) TOSCA Policy Type definition that is used to declare performance requirements for TOSCA nodes or groups of nodes.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_POLICIES_PERFORMANCE>`
    """
    
    DESCRIPTION = 'This is the default (root) TOSCA Policy Type definition that is used to declare performance requirements for TOSCA nodes or groups of nodes.'
