
from .utils.data import coerce_to_class
from aria import  dsl_specification
from collections import OrderedDict
from functools import total_ordering
import re

@total_ordering
class Version(object):
    # <major_version>.<minor_version>[.<fix_version>[.<qualifier>[-<build_version]]]
    RE = r'^(?P<major>\d+)\.(?P<minor>\d+)(\.(?P<fix>\d+)((\.(?P<qualifier>\d+))(\-(?P<build>\d+))?)?)?$'
    
    @staticmethod
    def key(version):
        """
        Key method for fast sorting.
        """
        return (version.major, version.minor, version.fix, version.qualifier, version.build)
    
    def __init__(self, entry_schema, constraints, value):
        match = re.match(Version.RE, value)
        if match is None:
            raise ValueError('version must be formatted as <major_version>.<minor_version>[.<fix_version>[.<qualifier>[-<build_version]]]')
        
        self.value = value
        
        self.major = match.group('major')
        self.major = int(self.major)
        self.minor = match.group('minor')
        self.minor = int(self.minor)
        self.fix = match.group('fix')
        self.fix = int(self.fix) if self.fix is not None else None
        self.qualifier = match.group('qualifier')
        self.qualifier = int(self.qualifier) if self.qualifier is not None else None
        self.build = match.group('build')
        self.build = int(self.build) if self.build is not None else None

    def __str__(self):
        return self.value
    
    def __eq__(self, version):
        return (self.major, self.minor, self.fix, self.qualifier, self.build) == (version.major, version.minor, version.fix, version.qualifier, version.build)

    def __lt__(self, version):
        if self.major < version.major:
            return True
        elif self.major == version.major:
            if self.minor < version.minor:
                return True
            elif self.minor == version.minor:
                if self.fix < version.fix:
                    return True
                elif self.fix == version.fix:
                    if self.qualifier < version.qualifier:
                        return True
                    elif self.qualifier == version.qualifier:
                        if self.build < version.build:
                            return True
        return False

@total_ordering
@dsl_specification('3.2.6', 'tosca-simple-profile-1.0')
class Scalar(object):
    """
    The scalar-unit type can be used to define scalar values along with a unit from the list of recognized units.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_SCALAR_UNIT>`__
    """

    @staticmethod
    def key(scalar):
        """
        Key method for fast sorting.
        """
        return scalar.value
    
    def __init__(self, entry_schema, constraints, value):
        match = re.match(self.__class__.RE, value)
        if match is None:
            raise ValueError('scalar be formatted as <scalar> <unit>')
        
        self.scalar = float(match.group('scalar'))
        self.unit = match.group('unit')
        self.value = self.__class__.TYPE(self.scalar * self.__class__.UNITS[self.unit])
    
    def __str__(self):
        return '%s %s' % (self.value, self.__class__.UNIT)
    
    def __eq__(self, scalar):
        return self.value == scalar.value

    def __lt__(self, scalar):
        return self.value < scalar.value

@dsl_specification('3.2.6.4', 'tosca-simple-profile-1.0')
class ScalarSize(Scalar):
    """
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_SCALAR_UNIT_SIZE>`__
    """

    # See: http://www.regular-expressions.info/floatingpoint.html
    RE = r'^(?P<scalar>[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s*(?P<unit>B|kB|KiB|MB|MiB|GB|GiB|TB|TiB)$'
    
    UNITS = {
        'B': 1,
        'kB': 1000,
        'KiB': 1024,
        'MB': 1000000,
        'MiB': 1048576,
        'GB': 1000000000,
        'GiB': 1073741824,
        'TB': 1000000000000,
        'TiB': 1099511627776}

    TYPE = int
    UNIT = 'bytes'

@dsl_specification('3.2.6.5', 'tosca-simple-profile-1.0')
class ScalarTime(Scalar):
    """
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_SCALAR_UNIT_TIME>`__
    """
    
    # See: http://www.regular-expressions.info/floatingpoint.html
    RE = r'^(?P<scalar>[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s*(?P<unit>ns|us|ms|s|m|h|d)$'

    UNITS = {
        'ns': 0.000000001,
        'us': 0.000001,
        'ms': 0.001,
        's': 1.0,
        'm': 60.0,
        'h': 3600.0,
        'd': 86400.0}

    TYPE = float
    UNIT = 'seconds'

@dsl_specification('3.2.6.6', 'tosca-simple-profile-1.0')
class ScalarFrequency(Scalar):
    """
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_SCALAR_UNIT_FREQUENCY>`__
    """
    
    # See: http://www.regular-expressions.info/floatingpoint.html
    RE = r'^(?P<scalar>[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s*(?P<unit>Hz|kHz|MHz|GHz)$'

    UNITS = {
        'Hz': 1.0,
        'kHz': 1000.0,
        'MHz': 1000000.0,
        'GHz': 1000000000.0}

    TYPE = float
    UNIT = 'Hz'

@dsl_specification('3.2.2', 'tosca-simple-profile-1.0')
def coerce_version(context, presentation, the_type, entry_schema, constraints, value):
    """
    TOSCA supports the concept of "reuse" of type definitions, as well as template definitions which could be version and change over time. It is important to provide a reliable, normative means to represent a version string which enables the comparison and management of types and templates over time. Therefore, the TOSCA TC intends to provide a normative version type (string) for this purpose in future Working Drafts of this specification.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_VERSION>`__
    """
    return coerce_to_class(context, presentation, Version, entry_schema, constraints, value)

@dsl_specification('3.2.3', 'tosca-simple-profile-1.0')
def coerce_range(context, presentation, the_type, entry_schema, constraints, value):
    """
    The range type can be used to define numeric ranges with a lower and upper boundary. For example, this allows for specifying a range of ports to be opened in a firewall.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_RANGE>`__
    """
    
    if not isinstance(value, list):
        # TODO must be list
        pass
    if len(value) != 2:
        # TODO must have 2 elements
        pass
    
    # first must be integer
    # second can be integer or UNBOUNDED
    # if second is integer, must be > first
    
    return value

@dsl_specification('3.2.4', 'tosca-simple-profile-1.0')
def coerce_list(context, presentation, the_type, entry_schema, constraints, value):
    """
    The list type allows for specifying multiple values for a parameter of property. For example, if an application allows for being configured to listen on multiple ports, a list of ports could be configured using the list data type.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_LIST>`__
    """
    
    if not isinstance(value, list):
        # TODO must be list
        pass

    return value
    
@dsl_specification('3.2.5', 'tosca-simple-profile-1.0')
def coerce_map_value(context, presentation, the_type, entry_schema, constraints, value):
    """
    The map type allows for specifying multiple values for a parameter of property as a map. In contrast to the list type, where each entry can only be addressed by its index in the list, entries in a map are named elements that can be addressed by their keys.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#TYPE_TOSCA_MAP>`__
    """
    
    if not isinstance(value, dict):
        # TODO must be dict
        pass
    
    r = OrderedDict()
    
    for k, v in value.iteritems():
        r[k] = v
    
    return r

def coerce_scalar_unit_size(context, presentation, the_type, entry_schema, constraints, value):
    return coerce_to_class(context, presentation, ScalarSize, entry_schema, constraints, value)

def coerce_scalar_unit_time(context, presentation, the_type, entry_schema, constraints, value):
    return coerce_to_class(context, presentation, ScalarTime, entry_schema, constraints, value)
    
def coerce_scalar_unit_frequency(context, presentation, the_type, entry_schema, constraints, value):
    return coerce_to_class(context, presentation, ScalarFrequency, entry_schema, constraints, value)
