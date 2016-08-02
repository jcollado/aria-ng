
from aria import dsl_specification, InvalidValueError, Issue
from aria.utils import ReadOnlyList

NODE_TEMPLATE_TARGET_SYMBOLS = ('SELF', 'HOST')
RELATIONSHIP_TEMPLATE_TARGET_SYMBOLS = ('SELF', 'SOURCE', 'TARGET')

class Function(object):
    def __init__(self, context, presentation, argument):
        pass
    
    def evaluate(self, context):
        return None

#
# Intrinsic
#

@dsl_specification('4.3.1', 'tosca-simple-profile-1.0')
class Concat(Function):
    """
    The concat function is used to concatenate two or more string values within a TOSCA service template.
    """

    def __init__(self, context, presentation, argument):
        if not isinstance(argument, list):
            raise InvalidValueError('function "concat" argument must be a list of string value expressions: %s' % repr(argument))
        
        string_value_expressions = []
        for a in argument:
            fn = get_function(context, presentation, a)
            if fn is not None:
                string_value_expressions.append(fn)
            else:
                string_value_expressions.append(a)
        self.string_value_expressions = ReadOnlyList(string_value_expressions)    

@dsl_specification('4.3.2', 'tosca-simple-profile-1.0')
class Token(Function):
    """
    The token function is used within a TOSCA service template on a string to parse out (tokenize) substrings separated by one or more token characters within a larger string.
    """

    def __init__(self, context, presentation, argument):
        if (not isinstance(argument, list)) or (len(argument) != 3):
            raise InvalidValueError('function "token" argument must be a list of 3 parameters: %s' % repr(argument))
        
        if not isinstance(argument[0], basestring):
            raise InvalidValueError('function "token" parameter 1 must be a string, the string to tokenize: %s' % repr(argument[0]))
        self.string_with_tokens = argument[0]
        
        if not isinstance(argument[1], basestring):
            raise InvalidValueError('function "token" parameter 2 must be a string, the token separator characters: %s' % repr(argument[1]))
        self.string_of_token_chars = argument[1]
        
        if not isinstance(argument[2], int):
            raise InvalidValueError('function "token" parameter 3 must be an integer, the 0-based index of the token to return: %s' % repr(argument[2]))
        self.substring_index = argument[2]

#
# Property
#

@dsl_specification('4.4.1', 'tosca-simple-profile-1.0')
class GetInput(Function):
    """
    The get\_input function is used to retrieve the values of properties declared within the inputs section of a TOSCA Service Template.
    """

    def __init__(self, context, presentation, argument):
        if not isinstance(argument, basestring):
            raise InvalidValueError('function "get_input" argument must be a string, the input property name: %s' % repr(argument))
        inputs = context.presentation.inputs
        if (inputs is None) or (argument not in inputs):
            raise InvalidValueError('function "get_input" argument is not a valid input name: %s' % repr(argument))
        self.input_property_name = argument

@dsl_specification('4.4.2', 'tosca-simple-profile-1.0')
class GetProperty(Function):
    """
    The get\_property function is used to retrieve property values between modelable entities defined in the same service template.
    """

    def __init__(self, context, presentation, argument):
        if (not isinstance(argument, list)) or (len(argument) < 2):
            raise InvalidValueError('function "get_property" argument must be a list of at least 2 parameters: %s' % repr(argument))
        
        if not isinstance(argument[0], basestring):
            raise InvalidValueError('function "get_property" parameter 1 must be a string, the modelable entity name: %s' % repr(argument[0]))
        self.modelable_entity_name = argument[0]
        
        if not isinstance(argument[1], basestring):
            raise InvalidValueError('function "get_property" parameter 2 must be a string, the (optional) requirement or capability name: %s' % repr(argument[1]))
        self.optional_req_or_cap_name = argument[1]

        if not isinstance(argument[2], basestring):
            raise InvalidValueError('function "get_property" parameter 3 must be a string, the property name: %s' % repr(argument[2]))
        self.property_name = argument[2]

        self.nested_property_name_or_index = argument[3:]

#
# Attribute
#

@dsl_specification('4.5.1', 'tosca-simple-profile-1.0')
class GetAttribute(Function):
    """
    The get\_attribute function is used to retrieve the values of named attributes declared by the referenced node or relationship template name.
    """

    def __init__(self, context, presentation, argument):
        if (not isinstance(argument, list)) or (len(argument) < 2):
            raise InvalidValueError('function "get_attribute" argument must be a list of 2 to 4 parameters: %s' % repr(argument))
        
        if not isinstance(argument[0], basestring):
            raise InvalidValueError('function "get_attribute" parameter 1 must be a string, the modelable entity name: %s' % repr(argument[0]))
        self.modelable_entity_name = argument[0]
        
        if not isinstance(argument[1], basestring):
            raise InvalidValueError('function "get_attribute" parameter 2 must be a string, the (optional) requirement or capability name: %s' % repr(argument[1]))
        self.optional_req_or_cap_name = argument[1]
        
        if not isinstance(argument[2], basestring):
            raise InvalidValueError('function "get_attribute" parameter 3 must be a string, the attribute name: %s' % repr(argument[2]))
        self.attribute_name = argument[2]
        
        self.nested_attribute_name_or_index = argument[3:]

#
# Operation
#

@dsl_specification('4.6.1', 'tosca-simple-profile-1.0')
class GetOperationOutput(Function):
    """
    The get\_operation\_output function is used to retrieve the values of variables exposed / exported from an interface operation.
    """

    def __init__(self, context, presentation, argument):
        if (not isinstance(argument, list)) or (len(argument) != 4):
            raise InvalidValueError('function "get_operation_output" argument must be a list of 4 parameters: %s' % repr(argument))

        if not isinstance(argument[0], basestring):
            raise InvalidValueError('function "get_operation_output" parameter 1 must be a string, the modelable entity name: %s' % repr(argument[0]))
        self.modelable_entity_name = argument[0]
        
        if not isinstance(argument[1], basestring):
            raise InvalidValueError('function "get_operation_output" parameter 2 must be a string, the interface name: %s' % repr(argument[1]))
        self.interface_name = argument[1]
        
        if not isinstance(argument[2], basestring):
            raise InvalidValueError('function "get_operation_output" parameter 3 must be a string, the operation name: %s' % repr(argument[2]))
        self.operation_name = argument[2]
        
        if not isinstance(argument[3], basestring):
            raise InvalidValueError('function "get_operation_output" parameter 4 must be a string, the output name: %s' % repr(argument[3]))
        self.output_variable_name = argument[3]

#
# Navigation
#

@dsl_specification('4.7.1', 'tosca-simple-profile-1.0')
class GetNodesOfType(Function):
    """
    The get\_nodes\_of\_type function can be used to retrieve a list of all known instances of nodes of the declared Node Type.
    """

    def __init__(self, context, presentation, argument):
        if not isinstance(argument, basestring):
            raise InvalidValueError('function "get_nodes_of_type" argument must be a string, the node type name: %s' % repr(argument))
        node_types = context.presentation.node_types
        if (node_types is None) or (argument not in node_types):
            raise InvalidValueError('function "get_nodes_of_type" argument is not a valid node type name: %s' % repr(argument))
        self.node_type_name = argument

#
# Artifact
#

@dsl_specification('4.8.1', 'tosca-simple-profile-1.0')
class GetArtifact(Function):
    """
    The get\_artifact function is used to retrieve artifact location between modelable entities defined in the same service template.
    """

    def __init__(self, context, presentation, argument):
        if (not isinstance(argument, list)) or (len(argument) < 2) or (len(argument) > 4):
            raise InvalidValueError('function "get_artifact" argument must be a list of 2 to 4 parameters: %s' % repr(argument))
        
        if not isinstance(argument[0], basestring):
            raise InvalidValueError('function "get_nodes_of_type" parameter 1 must be a string, the modelable entity name: %s' % repr(argument[0]))
        self.modelable_entity_name = argument[0]

        if not isinstance(argument[1], basestring):
            raise InvalidValueError('function "get_nodes_of_type" parameter 2 must be a string, the artifact name: %s' % repr(argument[1]))
        self.artifact_name = argument[1]
        
        if len(argument) > 2:
            if not isinstance(argument[2], basestring):
                raise InvalidValueError('function "get_nodes_of_type" parameter 3 must be a string, the location or "LOCAL_FILE": %s' % repr(argument[2]))
            self.location = argument[2]
        else:
            self.location = None
    
        if len(argument) > 3:
            if not isinstance(argument[3], bool):
                raise InvalidValueError('function "get_nodes_of_type" parameter 4 must be a boolean, the removal flag: %s' % repr(argument[2]))
            self.remove = argument[3]
        else:
            self.remove = None          

#
# Utils
#

FUNCTIONS = {
    'concat': Concat,
    'token': Token,
    'get_input': GetInput,
    'get_property': GetProperty,
    'get_attribute': GetAttribute,
    'get_operation_output': GetOperationOutput,
    'get_nodes_of_type': GetNodesOfType,
    'get_artifact': GetArtifact} 

def get_function(context, presentation, value):
    if isinstance(value, dict) and (len(value) == 1):
        key = value.keys()[0]
        if key in FUNCTIONS:
            try:
                return True, FUNCTIONS[key](context, presentation, value[key])
            except InvalidValueError as e:
                e.issue.locator = presentation._locator
                context.validation.report(issue=e.issue)
                return True, None
    return False, None

