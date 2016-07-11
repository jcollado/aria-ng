
from aria import dsl_specification, has_validated_properties
import tosca.interfaces
    
@has_validated_properties
@dsl_specification('5.7.4', 'tosca-simple-profile-1.0')
class Standard(tosca.interfaces.Root):
    """
    This lifecycle interface defines the essential, normative operations that TOSCA nodes may support.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#>`__ (wrong anchor)
    """

    SHORTHAND_NAME = 'Standard'
    TYPE_QUALIFIED_NAME = 'tosca:Standard'
    TYPE_URI = 'tosca.interfaces.node.lifecycle.Standard'
    
    def create(self, context):
        """
        Standard lifecycle create operation.
        """
    
    def configure(self, context):
        """
        Standard lifecycle configure operation.
        """
    
    def start(self, context):
        """
        Standard lifecycle start operation.
        """
    
    def stop(self, context):
        """
        Standard lifecycle stop operation.
        """
    
    def delete(self, context):
        """
        Standard lifecycle delete operation.
        """

__all__ = (
    'Standard',)
