
from utils import *

class String(object):
    YAML = 'tag:yaml.org,2002:str'
    
    SHORTHAND_NAME = 'string'
        
class Integer(HasConstraints):
    YAML = 'tag:yaml.org,2002:int'
    
    SHORTHAND_NAME = 'integer'

class Float(HasConstraints):
    YAML = 'tag:yaml.org,2002:float'
    
    SHORTHAND_NAME = 'float'

class Boolean(object):
    YAML = 'tag:yaml.org,2002:bool'
    
    SHORTHAND_NAME = 'boolean'

class Timestamp(object):
    YAML = 'tag:yaml.org,2002:timestamp'
    
    SHORTHAND_NAME = 'timestamp'

class Null(object):
    YAML = 'tag:yaml.org,2002:null'
    
    SHORTHAND_NAME = 'null'

class Version(object):
    """
    TOSCA supports the concept of "reuse" of type definitions, as well as template definitions which could be version and change over time. It is important to provide a reliable, normative means to represent a version string which enables the comparison and management of types and templates over time. Therefore, the TOSCA TC intends to provide a normative version type (string) for this purpose in future Working Drafts of this specification.
    """
    
    DESCRIPTION = 'TOSCA supports the concept of "reuse" of type definitions, as well as template definitions which could be version and change over time. It is important to provide a reliable, normative means to represent a version string which enables the comparison and management of types and templates over time. Therefore, the TOSCA TC intends to provide a normative version type (string) for this purpose in future Working Drafts of this specification.'
    
    SHORTHAND_NAME = 'version'
    TYPE_QUALIFIED_NAME = 'tosca:version'

class List(object):
    """
    The list type allows for specifying multiple values for a parameter of property. For example, if an application allows for being configured to listen on multiple ports, a list of ports could be configured using the list data type.
    
    Note that entries in a list for one property or parameter must be of the same type. The type (for simple entries) or schema (for complex entries) is defined by the entry_schema attribute of the respective property definition, attribute definitions, or input or output parameter definitions.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_LIST>`
    """
    
    DESCRIPTION = 'The list type allows for specifying multiple values for a parameter of property. For example, if an application allows for being configured to listen on multiple ports, a list of ports could be configured using the list data type.'

    SHORTHAND_NAME = 'list'
    TYPE_QUALIFIED_NAME = 'tosca:list'

    def __init__(self, type):
        self.type = type

class Map(object):
    """
    The map type allows for specifying multiple values for a parameter of property as a map. In contrast to the list type, where each entry can only be addressed by its index in the list, entries in a map are named elements that can be addressed by their keys.

    Note that entries in a map for one property or parameter must be of the same type. The type (for simple entries) or schema (for complex entries) is defined by the entry_schema attribute of the respective property definition, attribute definition, or input or output parameter definition.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_MAP>`
    """
    
    DESCRIPTION = 'The map type allows for specifying multiple values for a parameter of property as a map. In contrast to the list type, where each entry can only be addressed by its index in the list, entries in a map are named elements that can be addressed by their keys.'

    SHORTHAND_NAME = 'map'
    TYPE_QUALIFIED_NAME = 'tosca:map'

    def __init__(self, type):
        self.type = type

class Range(object):
    SHORTHAND_NAME = 'range'
    TYPE_QUALIFIED_NAME = 'tosca:range'

class Size(object):
    """
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_SCALAR_UNIT_SIZE>`
    """

    SHORTHAND_NAME = 'scalar-unit.size'
    TYPE_QUALIFIED_NAME = 'tosca:scalar-unit.size'

class Time(object):
    """
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_SCALAR_UNIT_TIME>`
    """
    
    SHORTHAND_NAME = 'scalar-unit.time'
    TYPE_QUALIFIED_NAME = 'tosca:scalar-unit.time'

class Frequency(object):
    """
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_SCALAR_UNIT_FREQUENCY>`
    """

    SHORTHAND_NAME = 'scalar-unit.frequency'
    TYPE_QUALIFIED_NAME = 'tosca:scalar-unit.frequency'
