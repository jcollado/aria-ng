
from aria import dsl_specification, has_validated_properties
import tosca
    
@has_validated_properties
@dsl_specification('5.9.1', 'tosca-simple-profile-1.0')
class Root(object):
    """
    This is the default (root) TOSCA Group Type definition that all other TOSCA base Group Types derive from.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#>`__ (no anchor)
    """

MODULES = (
    'nfv',)

__all__ = (
    'MODULES',
    'Root')
