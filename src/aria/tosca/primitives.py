
from aria import tosca_specification

@tosca_specification('3.2.1-1')
class String(object):
    """
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc373867862>`__
    """

    YAML = 'tag:yaml.org,2002:str'
    
    SHORTHAND_NAME = 'string'
        
@tosca_specification('3.2.1-2')
class Integer(object):
    """
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc373867862>`__
    """

    YAML = 'tag:yaml.org,2002:int'
    
    SHORTHAND_NAME = 'integer'
    
    #TODO constraints

@tosca_specification('3.2.1-3')
class Float(object):
    """
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc373867862>`__
    """

    YAML = 'tag:yaml.org,2002:float'
    
    SHORTHAND_NAME = 'float'

    #TODO constraints

@tosca_specification('3.2.1-4')
class Boolean(object):
    """
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc373867862>`__
    """

    YAML = 'tag:yaml.org,2002:bool'
    
    SHORTHAND_NAME = 'boolean'

@tosca_specification('3.2.1-5')
class Timestamp(object):
    """
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc373867862>`__
    """

    YAML = 'tag:yaml.org,2002:timestamp'
    
    SHORTHAND_NAME = 'timestamp'

@tosca_specification('3.2.1-6')
class Null(object):
    """
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc373867862>`__
    """

    YAML = 'tag:yaml.org,2002:null'
    
    SHORTHAND_NAME = 'null'

@tosca_specification('3.2.2')
class Version(object):
    """
    TOSCA supports the concept of "reuse" of type definitions, as well as template definitions which could be version and change over time. It is important to provide a reliable, normative means to represent a version string which enables the comparison and management of types and templates over time. Therefore, the TOSCA TC intends to provide a normative version type (string) for this purpose in future Working Drafts of this specification.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_VERSION>`__
    """
    
    SHORTHAND_NAME = 'version'
    TYPE_QUALIFIED_NAME = 'tosca:version'

@tosca_specification('3.2.4')
class List(object):
    """
    The list type allows for specifying multiple values for a parameter of property. For example, if an application allows for being configured to listen on multiple ports, a list of ports could be configured using the list data type.
    
    Note that entries in a list for one property or parameter must be of the same type. The type (for simple entries) or schema (for complex entries) is defined by the entry_schema attribute of the respective property definition, attribute definitions, or input or output parameter definitions.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_LIST>`__
    """

    SHORTHAND_NAME = 'list'
    TYPE_QUALIFIED_NAME = 'tosca:list'

    def __init__(self, type):
        self.type = type

@tosca_specification('3.2.5')
class Map(object):
    """
    The map type allows for specifying multiple values for a parameter of property as a map. In contrast to the list type, where each entry can only be addressed by its index in the list, entries in a map are named elements that can be addressed by their keys.

    Note that entries in a map for one property or parameter must be of the same type. The type (for simple entries) or schema (for complex entries) is defined by the entry_schema attribute of the respective property definition, attribute definition, or input or output parameter definition.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_MAP>`__
    """

    SHORTHAND_NAME = 'map'
    TYPE_QUALIFIED_NAME = 'tosca:map'

    def __init__(self, type):
        self.type = type

@tosca_specification('3.2.3')
class Range(object):
    """
    The range type can be used to define numeric ranges with a lower and upper boundary. For example, this allows for specifying a range of ports to be opened in a firewall.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_RANGE>`__
    """

    SHORTHAND_NAME = 'range'
    TYPE_QUALIFIED_NAME = 'tosca:range'

@tosca_specification('3.2.6.4')
class Size(object):
    """
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_SCALAR_UNIT_SIZE>`__
    """

    SHORTHAND_NAME = 'scalar-unit.size'
    TYPE_QUALIFIED_NAME = 'tosca:scalar-unit.size'

@tosca_specification('3.2.6.5')
class Time(object):
    """
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_SCALAR_UNIT_TIME>`__
    """
    
    SHORTHAND_NAME = 'scalar-unit.time'
    TYPE_QUALIFIED_NAME = 'tosca:scalar-unit.time'

@tosca_specification('3.2.6.6')
class Frequency(object):
    """
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_SCALAR_UNIT_FREQUENCY>`__
    """

    SHORTHAND_NAME = 'scalar-unit.frequency'
    TYPE_QUALIFIED_NAME = 'tosca:scalar-unit.frequency'
