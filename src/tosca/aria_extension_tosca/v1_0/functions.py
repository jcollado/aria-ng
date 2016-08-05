
from aria import dsl_specification, InvalidValueError, Issue
from aria.deployment import Function
from aria.utils import ReadOnlyList

NODE_TEMPLATE_TARGET_SYMBOLS = ('SELF', 'HOST')
RELATIONSHIP_TEMPLATE_TARGET_SYMBOLS = ('SELF', 'SOURCE', 'TARGET')
    
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
            raise InvalidValueError('function "concat" argument must be a list of string expressions: %s' % repr(argument))
        
        string_expressions = []
        for index in range(len(argument)):
            string_expressions.append(parse_string_expression(context, presentation, 'concat', index, None, argument[index]))
        self.string_expressions = ReadOnlyList(string_expressions)    

@dsl_specification('4.3.2', 'tosca-simple-profile-1.0')
class Token(Function):
    """
    The token function is used within a TOSCA service template on a string to parse out (tokenize) substrings separated by one or more token characters within a larger string.
    """

    def __init__(self, context, presentation, argument):
        if (not isinstance(argument, list)) or (len(argument) != 3):
            raise InvalidValueError('function "token" argument must be a list of 3 parameters: %s' % repr(argument))
        
        self.string_with_tokens = parse_string_expression(context, presentation, 'token', 0, 'the string to tokenize', argument[0])
        self.string_of_token_chars = parse_string_expression(context, presentation, 'token', 1, 'the token separator characters', argument[1])
        self.substring_index = parse_int(context, presentation, 'token', 2, 'the 0-based index of the token to return', argument[2])

#
# Property
#

@dsl_specification('4.4.1', 'tosca-simple-profile-1.0')
class GetInput(Function):
    """
    The get\_input function is used to retrieve the values of properties declared within the inputs section of a TOSCA Service Template.
    """

    def __init__(self, context, presentation, argument):
        self.input_property_name = parse_string_expression(context, presentation, 'get_input', None, 'the input property name', argument)

        if isinstance(self.input_property_name, basestring):
            inputs = context.presentation.inputs
            if (inputs is None) or (self.input_property_name not in inputs):
                raise InvalidValueError('function "get_input" argument is not a valid input name: %s' % repr(argument))
    
    def evaluate(self, context):
        input_definition = context.presentation.inputs.get(self.input_property_name)
        if input_definition is not None:
            return input_definition.value
        return None

@dsl_specification('4.4.2', 'tosca-simple-profile-1.0')
class GetProperty(Function):
    """
    The get\_property function is used to retrieve property values between modelable entities defined in the same service template.
    """

    def __init__(self, context, presentation, argument):
        if (not isinstance(argument, list)) or (len(argument) < 2):
            raise InvalidValueError('function "get_property" argument must be a list of at least 2 string expressions: %s' % repr(argument))

        self.modelable_entity_name = parse_modelable_entity_name(context, presentation, 'get_property', 0, argument[0])
        self.nested_property_name_or_index = argument[1:] # the first of these will be tried as a req-or-cap name

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
            raise InvalidValueError('function "get_attribute" argument must be a list of at least 2 string expressions: %s' % repr(argument))

        self.modelable_entity_name = parse_modelable_entity_name(context, presentation, 'get_attribute', 0, argument[0])
        self.nested_property_name_or_index = argument[1:] # the first of these will be tried as a req-or-cap name

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

        self.modelable_entity_name = parse_string_expression(context, presentation, 'get_operation_output', 0, 'modelable entity name', argument[0])
        self.interface_name = parse_string_expression(context, presentation, 'get_operation_output', 1, 'the interface name', argument[1])
        self.operation_name = parse_string_expression(context, presentation, 'get_operation_output', 2, 'the operation name', argument[2])
        self.output_variable_name = parse_string_expression(context, presentation, 'get_operation_output', 3, 'the output name', argument[3])

#
# Navigation
#

@dsl_specification('4.7.1', 'tosca-simple-profile-1.0')
class GetNodesOfType(Function):
    """
    The get\_nodes\_of\_type function can be used to retrieve a list of all known instances of nodes of the declared Node Type.
    """

    def __init__(self, context, presentation, argument):
        self.input_property_name = parse_string_expression(context, presentation, 'get_nodes_of_type', None, 'the node type name', argument)

        if isinstance(self.input_property_name, basestring):
            node_types = context.presentation.node_types
            if (node_types is None) or (self.input_property_name not in node_types):
                raise InvalidValueError('function "get_nodes_of_type" argument is not a valid node type name: %s' % repr(argument))

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

        self.modelable_entity_name = parse_string_expression(context, presentation, 'get_nodes_of_type', 0, 'modelable entity name', argument[0])
        self.artifact_name = parse_string_expression(context, presentation, 'get_nodes_of_type', 1, 'the artifact name', argument[1])
        self.location = parse_string_expression(context, presentation, 'get_nodes_of_type', 2, 'the location or "LOCAL_FILE"', argument[2])
        self.remove = parse_bool(context, presentation, 'get_nodes_of_type', 3, 'the removal flag', argument[3])

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

def get_self(presentation):
    from .templates import NodeTemplate, RelationshipTemplate
    
    if presentation is None:
        return None, None    
    elif isinstance(presentation, NodeTemplate):
        return presentation, 'node_template'
    elif isinstance(presentation, RelationshipTemplate):
        return presentation, 'relationship_template'
    else:
        return get_self(presentation._container)

def parse_string_expression(context, presentation, name, index, explanation, value):
    is_function, fn = get_function(context, presentation, value)
    if is_function:
        return fn
    else:
        value = str(value)
    return value

def parse_int(context, presentation, name, index, explanation, value):
    if not isinstance(value, int):
        try:
            value = int(value)
        except ValueError:
            raise invalid_value(name, index, 'an integer', explanation, value)
    return value

def parse_bool(context, presentation, name, index, explanation, value):
    if not isinstance(value, bool):
        raise invalid_value(name, index, 'a boolean', explanation, value)
    return value

@dsl_specification('4.1', 'tosca-simple-profile-1.0')
def parse_modelable_entity_name(context, presentation, name, index, value):
    value = parse_string_expression(context, presentation, name, index, 'the modelable entity name', value)
    if value == 'SELF':
        the_self, _ = get_self(presentation)
        if the_self is None:
            raise invalid_modelable_entity_name(name, index, value, 'a node template or a relationship template')
    elif value == 'HOST':
        _, self_variant = get_self(presentation)
        if self_variant != 'node_template':
            raise invalid_modelable_entity_name(name, index, value, 'a node template')
    elif (value == 'SOURCE') or (value == 'TARGET'):
        _, self_variant = get_self(presentation)
        if self_variant != 'relationship_template':
            raise invalid_modelable_entity_name(name, index, value, 'a relationship template')
    elif isinstance(value, basestring):
        node_templates = context.presentation.node_templates or {}
        relationship_templates = context.presentation.relationship_templates or {}
        if (value not in node_templates) and (value not in relationship_templates):
            raise InvalidValueError('function "%s" parameter %d is not a valid modelable entity name: %s' % (name, index + 1, repr(value)), level=Issue.BETWEEN_TYPES)
    return value

def invalid_modelable_entity_name(name, index, value, contexts):
    raise InvalidValueError('function "%s" parameter %d can be "%s" only in %s' % (name, index + 1, value, contexts), level=Issue.BETWEEN_TYPES)

def invalid_value(name, index, the_type, explanation, value):
    return InvalidValueError('function "%s" %s is not %s%s: %s' % (name, ('parameter %d' % (index + 1)) if index is not None else 'argument', the_type, (', %s' % explanation) if explanation is not None else '', repr(value)))
