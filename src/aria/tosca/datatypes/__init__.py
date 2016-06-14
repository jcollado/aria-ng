
from aria import tosca_specification, has_validated_properties, validated_property, property_type, property_default, required_property
import tosca

@has_validated_properties
@tosca_specification('5.2.1')
class Root(object):
    """
    This is the default (root) TOSCA Root Type definition that all complex TOSCA Data Types derive from.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_DATA_ROOT>`__
    """

@has_validated_properties
@tosca_specification('5.2.2')
class Credential(Root):
    """
    The Credential type is a complex TOSCA data Type used when describing authorization credentials used to access network accessible resources.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_DATA_CREDENTIAL>`__
    """

    SHORTHAND_NAME = 'Credential'
    TYPE_QUALIFIED_NAME = 'tosca:Credential'
    TYPE_URI = 'tosca.datatypes.Credential'
    
    @property_type(str)
    @validated_property
    def protocol():
        """
        The optional protocol name.
        """

    @required_property
    @property_default('password')
    @property_type(str)
    @validated_property
    def token_type():
        """
        The required token type.
        """

    @required_property
    @property_type(str)
    @validated_property
    def token():
        """
        The required token used as a credential for authorization or access to a networked resource.
        """

    @property_type(tosca.Map(str))
    @validated_property
    def keys():
        """
        The optional list of protocol-specific keys or assertions.
        """

    @property_type(str)
    @validated_property
    def user():
        """
        The optional user (name or ID) used for non-token based credentials.
        """
