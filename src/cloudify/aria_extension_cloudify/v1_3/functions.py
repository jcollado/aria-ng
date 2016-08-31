#
# Copyright (c) 2016 GigaSpaces Technologies Ltd. All rights reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#

from aria import Issue, InvalidValueError, dsl_specification
from aria.deployment import Function, CannotEvaluateFunction
from aria.utils import ReadOnlyList, deepclone
from cStringIO import StringIO

@dsl_specification('intrinsic-functions-1', 'cloudify-1.3')
class Concat(Function):
    """
    :code:`concat` is used for concatenating strings in different sections of the blueprint. :code:`concat` can be used in node properties, outputs, and node/relationship operation inputs. The function is evaluated once on deployment creation which will replace :code:`get_input` and :code:`get_property` usages; and it is evaluated on every operation execution and outputs evaluation, to replace usages of :code:`get_attribute` (if there are any).
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-intrinsic-functions/>`__.
    """

    def __init__(self, context, presentation, argument):
        self.locator = presentation._locator
        
        if not isinstance(argument, list):
            raise InvalidValueError('function "concat" argument must be a list of string expressions: %s' % repr(argument), locator=self.locator)
        
        string_expressions = []
        for index in range(len(argument)):
            string_expressions.append(parse_string_expression(context, presentation, 'concat', index, None, argument[index]))
        self.string_expressions = ReadOnlyList(string_expressions)    

    def _evaluate(self, context, container):
        r = StringIO()
        for e in self.string_expressions:
            if hasattr(e, '_evaluate'):
                e = e._evaluate(context, container)
            r.write(str(e))
        return r.getvalue()

@dsl_specification('intrinsic-functions-2', 'cloudify-1.3')
class GetInput(Function):
    """
    :code:`get_input` is used for referencing :code:`inputs` described in the inputs section of the blueprint. :code:`get_input` can be used in node properties, outputs, and node/relationship operation inputs. The function is evaluated on deployment creation.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-intrinsic-functions/>`__.
    """

    def __init__(self, context, presentation, argument):
        self.locator = presentation._locator

        self.input_property_name = parse_string_expression(context, presentation, 'get_input', None, 'the input property name', argument)

        if isinstance(self.input_property_name, basestring):
            inputs = context.presentation.inputs
            if (inputs is None) or (self.input_property_name not in inputs):
                raise InvalidValueError('function "get_input" argument is not a valid input name: %s' % repr(argument), locator=self.locator)
        
        self.context = context
    
    def _evaluate(self, context, container):
        if not hasattr(context.deployment, 'classic_plan'):
            raise CannotEvaluateFunction()

    def _evaluate_classic(self, classic_context):
        inputs = self.context.deployment.classic_plan['inputs']
        if self.input_property_name not in inputs:
            raise InvalidValueError('input does not exist for function "get_input": %s' % repr(self.input_property_name), locator=self.locator)
        return deepclone(inputs[self.input_property_name])

@dsl_specification('intrinsic-functions-3', 'cloudify-1.3')
class GetProperty(Function):
    """
    :code:`get_property` is used for referencing node properties within the blueprint. :code:`get_property` can be used in node properties, outputs, and node/relationship operation inputs. The function is evaluated on deployment creation.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-intrinsic-functions/>`__.
    """

    def __init__(self, context, presentation, argument):
        self.locator = presentation._locator
        
        if (not isinstance(argument, list)) or (len(argument) < 2):
            raise InvalidValueError('function "get_property" argument must be a list of at least 2 string expressions: %s' % repr(argument), locator=self.locator)

        self.modelable_entity_name = parse_modelable_entity_name(context, presentation, 'get_property', 0, argument[0])
        self.nested_property_name_or_index = argument[1:] # the first of these will be tried as a req-or-cap name

    def _evaluate(self, context, container):
        return ''

@dsl_specification('intrinsic-functions-4', 'cloudify-1.3')
class GetAttribute(Function):
    """
    :code:`get_attribute` is used to reference runtime-properties of different node-instances from within the blueprint.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-intrinsic-functions/>`__.
    """

    def __init__(self, context, presentation, argument):
        self.locator = presentation._locator

    def _evaluate(self, context, container):
        if not hasattr(context.deployment, 'classic_plan'):
            raise CannotEvaluateFunction()

    def _evaluate_classic(self, classic_context):
        # TODO
        return ''

#
# Utils
#

FUNCTIONS = {
    'concat': Concat,
    'get_input': GetInput,
    'get_property': GetProperty,
    'get_attribute': GetAttribute}

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

def parse_string_expression(context, presentation, name, index, explanation, value):
    is_function, fn = get_function(context, presentation, value)
    if is_function:
        return fn
    else:
        value = str(value)
    return value

def parse_modelable_entity_name(context, presentation, name, index, value):
    value = parse_string_expression(context, presentation, name, index, 'the modelable entity name', value)
    if value == 'SELF':
        the_self, _ = parse_self(presentation)
        if the_self is None:
            raise invalid_modelable_entity_name(name, index, value, presentation._locator, 'a node template or a relationship template')
    elif value == 'HOST':
        _, self_variant = parse_self(presentation)
        if self_variant != 'node_template':
            raise invalid_modelable_entity_name(name, index, value, presentation._locator, 'a node template')
    elif (value == 'SOURCE') or (value == 'TARGET'):
        _, self_variant = parse_self(presentation)
        if self_variant != 'relationship_template':
            raise invalid_modelable_entity_name(name, index, value, presentation._locator, 'a relationship template')
    elif isinstance(value, basestring):
        node_templates = context.presentation.node_templates or {}
        relationship_templates = context.presentation.relationship_templates or {}
        if (value not in node_templates) and (value not in relationship_templates):
            raise InvalidValueError('function "%s" parameter %d is not a valid modelable entity name: %s' % (name, index + 1, repr(value)), locator=presentation._locator, level=Issue.BETWEEN_TYPES)
    return value

def parse_self(presentation):
    from .templates import NodeTemplate, RelationshipTemplate
    
    if presentation is None:
        return None, None    
    elif isinstance(presentation, NodeTemplate):
        return presentation, 'node_template'
    elif isinstance(presentation, RelationshipTemplate):
        return presentation, 'relationship_template'
    else:
        return parse_self(presentation._container)

def invalid_modelable_entity_name(name, index, value, locator, contexts):
    return InvalidValueError('function "%s" parameter %d can be "%s" only in %s' % (name, index + 1, value, contexts), locator=locator, level=Issue.FIELD)
