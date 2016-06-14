
from aria import tosca_specification, has_validated_properties, validated_property, property_type, property_default, required_property
import tosca
    
@has_validated_properties
@tosca_specification('5.9.1')
class Root(object):
    """
    This is the default (root) TOSCA Group Type definition that all other TOSCA base Group Types derive from.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#>`__ (no anchor)
    """
