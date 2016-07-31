
from .presentation import ToscaPresentation
from .description import Description
from .field_validators import constraint_clause_field_validator, constraint_clause_in_range_validator, constraint_clause_valid_values_validator, constraint_clause_pattern_validator
from .utils.data import get_as_data_type, apply_constraint_to_value
from aria import dsl_specification
from aria.utils import cachedmethod
from aria.presentation import has_fields, short_form_field, primitive_field, primitive_list_field, object_field, field_validator

@has_fields
@dsl_specification('3.9.3.2', 'tosca-simple-profile-1.0')
class MetaData(ToscaPresentation):
    @primitive_field(str)
    @dsl_specification('3.9.3.3', 'tosca-simple-profile-1.0')
    def template_name(self):
        """
        This optional metadata keyname can be used to declare the name of service template as a single-line string value.
        """

    @primitive_field(str)
    @dsl_specification('3.9.3.4', 'tosca-simple-profile-1.0')
    def template_author(self):
        """
        This optional metadata keyname can be used to declare the author(s) of the service template as a single-line string value.
        """

    @primitive_field(str)
    @dsl_specification('3.9.3.5', 'tosca-simple-profile-1.0')
    def template_version(self):
        """
        This optional metadata keyname can be used to declare a domain specific version of the service template as a single-line string value.
        """

@has_fields
@dsl_specification('3.5.5', 'tosca-simple-profile-1.0')
class Repository(ToscaPresentation):
    """
    A repository definition defines a named external repository which contains deployment and implementation artifacts that are referenced within the TOSCA Service Template.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_REPOSITORY_DEF>`__
    """

    @object_field(Description)
    def description(self):
        """
        The optional description for the repository.
        
        :rtype: :class:`Description`
        """

    @primitive_field(str, required=True)
    def url(self):
        """
        The required URL or network address used to access the repository.
        
        :rtype: str
        """

    @primitive_field()
    def credential(self):
        """
        The optional Credential used to authorize access to the repository.
        
        :rtype: tosca.datatypes.Credential
        """
    
    @cachedmethod
    def _get_credential(self, context):
        return get_as_data_type(context, self, 'credential', 'tosca.datatypes.Credential')

@short_form_field('file')
@has_fields
@dsl_specification('3.5.7', 'tosca-simple-profile-1.0')
class Import(ToscaPresentation):
    """
    An import definition is used within a TOSCA Service Template to locate and uniquely name another TOSCA Service Template file which has type and template definitions to be imported (included) and referenced within another Service Template.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_IMPORT_DEF>`__
    """
    
    @primitive_field(str, required=True)
    def file(self):
        """
        The required symbolic name for the imported file.
        
        :rtype: str
        """

    @primitive_field(str)
    def repository(self):
        """
        The optional symbolic name of the repository definition where the imported file can be found as a string.
        
        :rtype: str
        """

    @primitive_field(str)
    def namespace_uri(self):
        """
        The optional namespace URI to that will be applied to type definitions found within the imported file as a string.
        
        :rtype: str
        """

    @primitive_field(str)
    def namespace_prefix(self):
        """
        The optional namespace prefix (alias) that will be used to indicate the namespace_uri when forming a qualified name (i.e., qname) when referencing type definitions from the imported file.
        
        :rtype: str
        """

    #def _dump(self, context):
    #    puts('Import:')
    #    with context.style.indent:
    #        if self.credential:
    #            puts('File: %s' % context.style.literal(self.credential))

@has_fields
@dsl_specification('3.5.2', 'tosca-simple-profile-1.0')
class ConstraintClause(ToscaPresentation):
    """
    A constraint clause defines an operation along with one or more compatible values that can be used to define a constraint on a property or parameter's allowed values when it is defined in a TOSCA Service Template or one of its entities.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_CONSTRAINTS_CLAUSE>`__
    """
    
    @field_validator(constraint_clause_field_validator)
    @primitive_field()
    def equal(self):
        """
        Constrains a property or parameter to a value equal to ('=') the value declared.
        """
    
    @field_validator(constraint_clause_field_validator)
    @primitive_field()
    def greater_than(self):
        """
        Constrains a property or parameter to a value greater than ('>') the value declared.
        """
    
    @field_validator(constraint_clause_field_validator)
    @primitive_field()
    def greater_or_equal(self):
        """
        Constrains a property or parameter to a value greater than or equal to ('>=') the value declared.
        """
    
    @field_validator(constraint_clause_field_validator)
    @primitive_field()
    def less_than(self):
        """
        Constrains a property or parameter to a value less than ('<') the value declared.
        """
    
    @field_validator(constraint_clause_field_validator)
    @primitive_field()
    def less_or_equal(self):
        """
        Constrains a property or parameter to a value less than or equal to ('<=') the value declared.
        """
    
    @field_validator(constraint_clause_in_range_validator)
    @primitive_list_field()
    def in_range(self):
        """
        Constrains a property or parameter to a value in range of (inclusive) the two values declared.

        Note: subclasses or templates of types that declare a property with the in_range constraint MAY only further restrict the range specified by the parent type.
        """
    
    @field_validator(constraint_clause_valid_values_validator)
    @primitive_list_field()
    def valid_values(self):
        """
        Constrains a property or parameter to a value that is in the list of declared values.
        """
    
    @primitive_field(int)
    def length(self):
        """
        Constrains the property or parameter to a value of a given length.
        """
    
    @primitive_field(int)
    def min_length(self):
        """
        Constrains the property or parameter to a value to a minimum length.
        """
    
    @primitive_field(int)
    def max_length(self):
        """
        Constrains the property or parameter to a value to a maximum length.
        """

    @field_validator(constraint_clause_pattern_validator)
    @primitive_field(str)
    def pattern(self):
        """
        Constrains the property or parameter to a value that is allowed by the provided regular expression.

        Note: Future drafts of this specification will detail the use of regular expressions and reference an appropriate standardized grammar.
        """
    
    @cachedmethod
    def _get_type(self, context):
        if hasattr(self._container, '_get_type_for_name'):
            return self._container._get_type_for_name(context, self._name)
        elif hasattr(self._container, '_get_type'):
            return self._container._get_type(context)
        else:
            # We are inside DataType, so the DataType itself is our type 
            return self._container
    
    @cachedmethod
    def _is_typed(self):
        key = self._raw.keys()[0]
        return key in ('equal', 'greater_than', 'greater_or_equal', 'less_than', 'less_or_equal', 'less_or_equal', 'in_range', 'valid_values')
                
    def _apply_to_value(self, context, presentation, value):
        return apply_constraint_to_value(context, presentation, self, value)
