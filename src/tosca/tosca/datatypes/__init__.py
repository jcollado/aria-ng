
from aria import dsl_specification, has_validated_properties, validated_property
import tosca

@has_validated_properties
@dsl_specification('5.2.1', 'tosca-simple-profile-1.0')
class Root(object):
    """
    This is the default (root) TOSCA Root Type definition that all complex TOSCA Data Types derive from.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_DATA_ROOT>`__
    """

@has_validated_properties
@dsl_specification('5.2.2', 'tosca-simple-profile-1.0')
class Credential(Root):
    """
    The Credential type is a complex TOSCA data Type used when describing authorization credentials used to access network accessible resources.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_DATA_CREDENTIAL>`__
    """

    SHORTHAND_NAME = 'Credential'
    TYPE_QUALIFIED_NAME = 'tosca:Credential'
    TYPE_URI = 'tosca.datatypes.Credential'
    
    @validated_property(str)
    def protocol(self):
        """
        The optional protocol name.
        """

    @validated_property(str, default='password', required=True)
    def token_type(self):
        """
        The required token type.
        """

    @validated_property(str, required=True)
    def token(self):
        """
        The required token used as a credential for authorization or access to a networked resource.
        """

    @validated_property(tosca.Map(str))
    def keys(self):
        """
        The optional list of protocol-specific keys or assertions.
        """

    @validated_property(str)
    def user(self):
        """
        The optional user (name or ID) used for non-token based credentials.
        """

MODULES = (
    'compute',
    'network')

__all__ = (
    'MODULES',
    'Root',
    'Credential')
