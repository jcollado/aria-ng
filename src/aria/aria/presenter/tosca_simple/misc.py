
from aria import tosca_specification, has_fields, primitive_field, object_field, field_type, field_getter, required_field
from aria.presenter import Presentation
from tosca.datatypes import Credential

@has_fields
@tosca_specification('3.5.5')
class Repository(Presentation):
    """
    A repository definition defines a named external repository which contains deployment and implementation artifacts that are referenced within the TOSCA Service Template.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_REPOSITORY_DEF>`__
    """
    
    @field_type(str)
    @primitive_field
    def description():
        """
        The optional description for the repository.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

    @required_field
    @field_type(str)
    @primitive_field
    def url():
        """
        The required URL or network address used to access the repository.
        
        :rtype: str
        """

    @object_field(Credential)
    def credential():
        """
        The optional Credential used to authorize access to the repository.
        
        :rtype: :class:`tosca.datatypes.Credential`
        """

def get_file(field, raw):
    if isinstance(raw, basestring):
        return raw
    else:
        return field._get(raw)

@has_fields
@tosca_specification('3.5.7')
class Import(Presentation):
    """
    An import definition is used within a TOSCA Service Template to locate and uniquely name another TOSCA Service Template file which has type and template definitions to be imported (included) and referenced within another Service Template.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_IMPORT_DEF>`__
    """
    
    @required_field
    @field_type(str)
    @field_getter(get_file)
    @primitive_field
    def file():
        """
        The required symbolic name for the imported file.
        
        :rtype: str
        """

    @field_type(str)
    @primitive_field
    def repository():
        """
        The optional symbolic name of the repository definition where the imported file can be found as a string.
        
        :rtype: str
        """

    @field_type(str)
    @primitive_field
    def namespace_uri():
        """
        The optional namespace URI to that will be applied to type definitions found within the imported file as a string.
        
        :rtype: str
        """

    @field_type(str)
    @primitive_field
    def namespace_prefix():
        """
        The optional namespace prefix (alias) that will be used to indicate the namespace_uri when forming a qualified name (i.e., qname) when referencing type definitions from the imported file.
        
        :rtype: str
        """

@has_fields
@tosca_specification('3.5.2')
class ConstraintClause(Presentation):
    """
    A constraint clause defines an operation along with one or more compatible values that can be used to define a constraint on a property or parameter's allowed values when it is defined in a TOSCA Service Template or one of its entities.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_CONSTRAINTS_CLAUSE>`__
    """
    
    @primitive_field
    def equal():
        """
        Constrains a property or parameter to a value equal to ('=') the value declared.
        """
    
    @primitive_field
    def greater_than():
        """
        Constrains a property or parameter to a value greater than ('>') the value declared.
        """
    
    @primitive_field
    def greater_or_equal():
        """
        Constrains a property or parameter to a value greater than or equal to ('>=') the value declared.
        """
    
    @primitive_field
    def less_than():
        """
        Constrains a property or parameter to a value less than ('<') the value declared.
        """
    
    @primitive_field
    def less_or_equal():
        """
        Constrains a property or parameter to a value less than or equal to ('<=') the value declared.
        """
    
    @primitive_field
    def in_range():
        """
        Constrains a property or parameter to a value in range of (inclusive) the two values declared.

        Note: subclasses or templates of types that declare a property with the in_range constraint MAY only further restrict the range specified by the parent type.
        """
    
    @primitive_field
    def valid_values():
        """
        Constrains a property or parameter to a value that is in the list of declared values.
        """
    
    @primitive_field
    def length():
        """
        Constrains the property or parameter to a value of a given length.
        """
    
    @primitive_field
    def min_length():
        """
        Constrains the property or parameter to a value to a minimum length.
        """
    
    @primitive_field
    def max_length():
        """
        Constrains the property or parameter to a value to a maximum length.
        """

    @primitive_field
    def pattern():
        """
        Constrains the property or parameter to a value that is allowed by the provided regular expression.

        Note: Future drafts of this specification will detail the use of regular expressions and reference an appropriate standardized grammar.
        """
