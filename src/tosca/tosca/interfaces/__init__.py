
from aria import dsl_specification, has_validated_properties
import tosca
    
@has_validated_properties
@dsl_specification('5.7.3', 'tosca-simple-profile-1.0')
class Root(object):
    """
    This is the default (root) TOSCA Interface Type definition that all other TOSCA Interface Types derive from.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Ref384391055>`__ (wrong anchor)
    """
    
MODULES = (
    'node',)

__all__ = (
    'MODULES',
    'Root')
