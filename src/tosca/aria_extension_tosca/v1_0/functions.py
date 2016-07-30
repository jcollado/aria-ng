
from aria import dsl_specification

#
# Intrinsic
#

@dsl_specification('4.3.1', 'tosca-simple-profile-1.0')
class Concat(object):
    """
    The concat function is used to concatenate two or more string values within a TOSCA service template.
    """

@dsl_specification('4.3.2', 'tosca-simple-profile-1.0')
class Token(object):
    """
    The token function is used within a TOSCA service template on a string to parse out (tokenize) substrings separated by one or more token characters within a larger string.
    """

#
# Property
#

@dsl_specification('4.4.1', 'tosca-simple-profile-1.0')
class GetInput(object):
    """
    The get\_input function is used to retrieve the values of properties declared within the inputs section of a TOSCA Service Template.
    """

@dsl_specification('4.4.2', 'tosca-simple-profile-1.0')
class GetProperty(object):
    """
    The get\_property function is used to retrieve property values between modelable entities defined in the same service template.
    """

#
# Attribute
#

@dsl_specification('4.5.1', 'tosca-simple-profile-1.0')
class GetAttribute(object):
    """
    The get\_attribute function is used to retrieve the values of named attributes declared by the referenced node or relationship template name.
    """

#
# Operation
#

@dsl_specification('4.6.1', 'tosca-simple-profile-1.0')
class GetOperationOutput(object):
    """
    The get\_operation\_output function is used to retrieve the values of variables exposed / exported from an interface operation.
    """

#
# Navigation
#

@dsl_specification('4.7.1', 'tosca-simple-profile-1.0')
class GetNodesOfType(object):
    """
    The get\_nodes\_of\_type function can be used to retrieve a list of all known instances of nodes of the declared Node Type.
    """

#
# Artifact
#

@dsl_specification('4.8.1', 'tosca-simple-profile-1.0')
class GetArtifact(object):
    """
    The get\_artifact function is used to retrieve artifact location between modelable entities defined in the same service template.
    """

FUNCTIONS = {
    'concat': Concat,
    'token': Token,
    'get_input': GetInput,
    'get_property': GetProperty,
    'get_attribute': GetAttribute,
    'get_operation_output': GetOperationOutput,
    'get_nodes_of_type': GetNodesOfType,
    'get_artifact': GetArtifact} 
