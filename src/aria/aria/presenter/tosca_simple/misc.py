
from base import Base
from tosca import Range
from tosca.datatypes import Credential

class Repository(Base):
    """
    A repository definition defines a named external repository which contains deployment and implementation artifacts that are referenced within the TOSCA Service Template.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_REPOSITORY_DEF>`__
    """
    
    REQUIRED = ['url']
    
    @property
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
        return self._get_primitive('description')

    @property
    def url(self):
        return self._get_primitive('url')

    @property
    def credential(self):
        """
        :class:`tosca.datatypes.Credential`
        """
        return self._get_object('credential', Credential)

class Import(Base):
    """
    An import definition is used within a TOSCA Service Template to locate and uniquely name another TOSCA Service Template file which has type and template definitions to be imported (included) and referenced within another Service Template.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_IMPORT_DEF>`__
    """
    
    REQUIRED = ['file']

    def __init__(self, raw={}):
        super(Import, self).__init__({'file': raw} if isinstance(raw, basestring) else raw)

    @property
    def file(self):
        return self._get_primitive('file')

    @file.setter
    def file(self, value):
        self.raw['file'] = value

    @property
    def repository(self):
        return self._get_primitive('repository')

    @repository.setter
    def repository(self, value):
        self.raw['repository'] = value

    @property
    def namespace_uri(self):
        return self._get_primitive('namespace_uri')

    @namespace_uri.setter
    def namespace_uri(self, value):
        self.raw['namespace_uri'] = value

    @property
    def namespace_prefix(self):
        return self._get_primitive('namespace_prefix')

    @namespace_prefix.setter
    def namespace_prefix(self, value):
        self.raw['namespace_prefix'] = value

class ConstraintClause(Base):
    """
    A constraint clause defines an operation along with one or more compatible values that can be used to define a constraint on a property or parameter's allowed values when it is defined in a TOSCA Service Template or one of its entities.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_CONSTRAINTS_CLAUSE>`__
    """
    
    @property
    def equal(self):
        return self._get_primitive('equal')
    
    @property
    def greater_than(self):
        return self._get_primitive('greater_than')
    
    @property
    def greater_or_equal(self):
        return self._get_primitive('greater_or_equal')
    
    @property
    def less_than(self):
        return self._get_primitive('less_than')
    
    @property
    def less_or_equal(self):
        return self._get_primitive('less_or_equal')
    
    @property
    def in_range(self):
        return self._get_object('in_range', Range)
    
    @property
    def valid_values(self):
        return self._get_primitive_list('valid_values')
    
    @property
    def length(self):
        return self._get_primitive('length')
    
    @property
    def min_length(self):
        return self._get_primitive('min_length')
    
    @property
    def max_length(self):
        return self._get_primitive('max_length')

    @property
    def pattern(self):
        return self._get_primitive('pattern')
