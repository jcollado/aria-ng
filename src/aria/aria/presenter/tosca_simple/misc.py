
from aria.presenter import Presentation, has_fields, primitive_field, object_field, field_type, field_getter, required_field
from tosca.datatypes import Credential

@has_fields
class Repository(Presentation):
    """
    A repository definition defines a named external repository which contains deployment and implementation artifacts that are referenced within the TOSCA Service Template.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_REPOSITORY_DEF>`__
    """
    
    @field_type(str)
    @primitive_field
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @required_field
    @field_type(str)
    @primitive_field
    def url(self):
        pass

    @object_field(Credential)
    def credential(self):
        """
        :class:`tosca.datatypes.Credential`
        """

def get_file(field, raw):
    if isinstance(raw, basestring):
        return raw
    else:
        return field._get(raw)

@has_fields
class Import(Presentation):
    """
    An import definition is used within a TOSCA Service Template to locate and uniquely name another TOSCA Service Template file which has type and template definitions to be imported (included) and referenced within another Service Template.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_IMPORT_DEF>`__
    """
    
    @required_field
    @field_type(str)
    @field_getter(get_file)
    @primitive_field
    def file(self):
        pass

    @field_type(str)
    @primitive_field
    def repository(self):
        pass

    @field_type(str)
    @primitive_field
    def namespace_uri(self):
        pass

    @field_type(str)
    @primitive_field
    def namespace_prefix(self):
        pass

@has_fields
class ConstraintClause(Presentation):
    """
    A constraint clause defines an operation along with one or more compatible values that can be used to define a constraint on a property or parameter's allowed values when it is defined in a TOSCA Service Template or one of its entities.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_CONSTRAINTS_CLAUSE>`__
    """
    
    @primitive_field
    def equal(self):
        pass
    
    @primitive_field
    def greater_than(self):
        pass
    
    @primitive_field
    def greater_or_equal(self):
        pass
    
    @primitive_field
    def less_than(self):
        pass
    
    @primitive_field
    def less_or_equal(self):
        pass
    
    @primitive_field
    def in_range(self):
        pass
    
    @primitive_field
    def valid_values(self):
        pass
    
    @primitive_field
    def length(self):
        pass
    
    @primitive_field
    def min_length(self):
        pass
    
    @primitive_field
    def max_length(self):
        pass

    @primitive_field
    def pattern(self):
        pass
