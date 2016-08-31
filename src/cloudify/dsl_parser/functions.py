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

from aria.utils import deepclone

def evaluate_outputs(outputs_def, get_node_instances_method, get_node_instance_method, get_node_method):
    """
    Evaluates an outputs definition containing intrinsic functions.

    :param outputs_def: Outputs definition.
    :param get_node_instances_method: A method for getting node instances.
    :param get_node_instance_method: A method for getting a node instance.
    :param get_node_method: A method for getting a node.
    :return: Outputs dict.
    """
    print '!!! evaluate_outputs'
    
def evaluate_functions(payload, context, get_node_instances_method, get_node_instance_method, get_node_method):
    """
    Evaluate functions in payload.

    :param payload: The payload to evaluate.
    :param context: Context used during evaluation.
    :param get_node_instances_method: A method for getting node instances.
    :param get_node_instance_method: A method for getting a node instance.
    :param get_node_method: A method for getting a node.
    :return: payload.
    """
    
    #print '!!! evaluate_function', payload, context    
    #node_id = context.get('self')
    
    r = {}
    if payload:
        for name, value in payload.iteritems():
            r[name] = _evaluate_functions(context, value['default'])
            # TODO: coerce to type?
    
    return r    

#
# Utils
#

def _evaluate_functions(classic_context, value):
    if hasattr(value, '_evaluate_classic'):
        value = value._evaluate_classic(classic_context)
    else:
        value = deepclone(value)
    
    if isinstance(value, dict):
        for k, v in value.iteritems():
            value[k] = _evaluate_functions(classic_context, v)
    elif isinstance(value, list):
        for i in range(len(value)):
            value[i] = _evaluate_functions(classic_context, value[i])
            
    return value
