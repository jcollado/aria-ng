
import tosca
    
class Root(tosca.HasProperties):
    """
    This is the default (root) TOSCA Group Type definition that all other TOSCA base Group Types derive from.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#>`__ (no anchor)
    """
    
    DESCRIPTION = 'This is the default (root) TOSCA Group Type definition that all other TOSCA base Group Types derive from.'
