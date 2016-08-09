
from aria import dsl_specification, InvalidValueError
from aria.deployment import Function

@dsl_specification('intrinsic-functions-1', 'cloudify-1.3')
class Concat(Function):
    """
    :code:`concat` is used for concatenating strings in different sections of the blueprint. :code:`concat` can be used in node properties, outputs, and node/relationship operation inputs. The function is evaluated once on deployment creation which will replace :code:`get_input` and :code:`get_property` usages; and it is evaluated on every operation execution and outputs evaluation, to replace usages of :code:`get_attribute` (if there are any).
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-intrinsic-functions/>`__.
    """

    def __init__(self, context, presentation, argument):
        self.locator = presentation._locator


@dsl_specification('intrinsic-functions-2', 'cloudify-1.3')
class GetInput(Function):
    """
    :code:`get_input` is used for referencing :code:`inputs` described in the inputs section of the blueprint. :code:`get_input` can be used in node properties, outputs, and node/relationship operation inputs. The function is evaluated on deployment creation.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-intrinsic-functions/>`__.
    """

    def __init__(self, context, presentation, argument):
        self.locator = presentation._locator

@dsl_specification('intrinsic-functions-3', 'cloudify-1.3')
class GetProperty(Function):
    """
    :code:`get_property` is used for referencing node properties within the blueprint. :code:`get_property` can be used in node properties, outputs, and node/relationship operation inputs. The function is evaluated on deployment creation.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-intrinsic-functions/>`__.
    """

    def __init__(self, context, presentation, argument):
        self.locator = presentation._locator

@dsl_specification('intrinsic-functions-4', 'cloudify-1.3')
class GetAttribute(Function):
    """
    :code:`get_attribute` is used to reference runtime-properties of different node-instances from within the blueprint.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-intrinsic-functions/>`__.
    """

    def __init__(self, context, presentation, argument):
        self.locator = presentation._locator

#
# Utils
#

FUNCTIONS = {
    'get_input': GetInput,
    'get_property': GetProperty}

def get_function(context, presentation, value):
    if isinstance(value, dict) and (len(value) == 1):
        key = value.keys()[0]
        if key in FUNCTIONS:
            try:
                return True, FUNCTIONS[key](context, presentation, value[key])
            except InvalidValueError as e:
                context.validation.report(issue=e.issue)
                return True, None
    return False, None
