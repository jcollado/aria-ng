
import tosca
    
class Root(tosca.HasProperties):
    """
    This is the default (root) TOSCA Root Type definition that all complex TOSCA Data Types derive from.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_DATA_ROOT>`
    """
    
    DESCRIPTION = 'This is the default (root) TOSCA Root Type definition that all complex TOSCA Data Types derive from.'

class Credential(Root):
    """
    The Credential type is a complex TOSCA data Type used when describing authorization credentials used to access network accessible resources.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_DATA_CREDENTIAL>`
    """

    DESCRIPTION = 'The Credential type is a complex TOSCA data Type used when describing authorization credentials used to access network accessible resources.'

    SHORTHAND_NAME = 'Credential'
    TYPE_QUALIFIED_NAME = 'tosca:Credential'
    TYPE_URI = 'tosca.datatypes.Credential'
    
    PROPERTIES = {
        'protocol': {'type': str, 'description': 'The optional protocol name.'},
        'token_type': {'type': str, 'required': True, 'default': 'password', 'description': 'The required token type.'},
        'token': {'type': str, 'required': True, 'description': 'The required token used as a credential for authorization or access to a networked resource.'},
        'keys': {'type': tosca.Map(str), 'description': 'The optional list of protocol-specific keys or assertions.'},
        'user': {'type': str, 'description': 'The optional user (name or ID) used for non-token based credentials.'}}
