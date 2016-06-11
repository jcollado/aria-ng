
from aria.presenter import HasRaw, has_properties, property_primitive, property_object, required
from tosca.datatypes import Credential

@has_properties
class Repository(HasRaw):
    """
    A repository definition defines a named external repository which contains deployment and implementation artifacts that are referenced within the TOSCA Service Template.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_REPOSITORY_DEF>`__
    """
    
    @property_primitive
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @required
    @property_primitive
    def url(self):
        pass

    @property_object(Credential)
    def credential(self):
        """
        :class:`tosca.datatypes.Credential`
        """

@has_properties
class Import(HasRaw):
    """
    An import definition is used within a TOSCA Service Template to locate and uniquely name another TOSCA Service Template file which has type and template definitions to be imported (included) and referenced within another Service Template.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_IMPORT_DEF>`__
    """
    
    def __init__(self, raw={}):
        super(Import, self).__init__({'file': raw} if isinstance(raw, basestring) else raw)

    @required
    @property_primitive
    def file(self):
        pass

    @property_primitive
    def repository(self):
        pass

    @property_primitive
    def namespace_uri(self):
        pass

    @property_primitive
    def namespace_prefix(self):
        pass

@has_properties
class ConstraintClause(HasRaw):
    """
    A constraint clause defines an operation along with one or more compatible values that can be used to define a constraint on a property or parameter's allowed values when it is defined in a TOSCA Service Template or one of its entities.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_CONSTRAINTS_CLAUSE>`__
    """
    
    @property_primitive
    def equal(self):
        pass
    
    @property_primitive
    def greater_than(self):
        pass
    
    @property_primitive
    def greater_or_equal(self):
        pass
    
    @property_primitive
    def less_than(self):
        pass
    
    @property_primitive
    def less_or_equal(self):
        pass
    
    @property_primitive
    def in_range(self):
        pass
    
    @property_primitive
    def valid_values(self):
        pass
    
    @property_primitive
    def length(self):
        pass
    
    @property_primitive
    def min_length(self):
        pass
    
    @property_primitive
    def max_length(self):
        pass

    @property_primitive
    def pattern(self):
        pass
