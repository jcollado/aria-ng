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

from aria.consumption import Plan as BasicPlan
from aria.deployment import Parameter, Function
from aria.utils import JSONValueEncoder, deepclone
from collections import OrderedDict
import json

class Plan(BasicPlan):
    """
    Emits the deployment plan instantiated from the deployment template.
    """

    def consume(self):
        self.create_deployment_plan()
        if not self.context.validation.has_issues:
            self.create_classic_plan()
            if self.context.deployment.classic_plan is not None:
                print json.dumps(self.context.deployment.classic_plan, indent=2, cls=JSONValueEncoder)

    def create_classic_plan(self):
        classic_plan = None
        if (self.context.deployment.plan is not None):
            classic_plan = convert_plan(self.context)
        setattr(self.context.deployment, 'classic_plan', classic_plan)

#
# Conversions
#

def convert_plan(context):
    r = OrderedDict((
        ('description', context.deployment.plan.description),
        ('inputs', convert_properties(context, context.deployment.plan.inputs)),
        ('outputs', convert_properties(context, context.deployment.plan.outputs)),
        ('nodes', [convert_node_template(context, value) for value in context.deployment.template.node_templates.itervalues()]),
        ('node_instances', [convert_node(context, v) for v in context.deployment.plan.nodes.itervalues()]),
        ('scaling_groups', OrderedDict(
            (k, convert_group_template(context, v)) for k, v in context.deployment.template.group_templates.iteritems())),
        ('workflows', OrderedDict(
            (k, convert_operation(context, v, True)) for k, v in context.deployment.plan.operations.iteritems())),
        ('relationships', OrderedDict(
            (relationship_type.name, convert_relationship_type(context, relationship_type)) for relationship_type in context.deployment.relationship_types.iter_descendants()))))

    # TODO
    #setattr(version, 'raw', version['raw'])
    #setattr(version, 'definitions_name', version['definitions_name'])
    #setattr(version, 'definitions_version', version['definitions_version'])
    
    #setattr(r, 'version', r['version'])
    setattr(r, 'inputs', r['inputs'])
    setattr(r, 'outputs', r['outputs'])
    setattr(r, 'node_templates', r['nodes'])
    
    return r

def convert_node_template(context, node_template):
    node_type = context.deployment.node_types.get_descendant(node_template.type_name)
    host_node_template = find_host_node_template(context, node_template)
    
    current_instances = 0
    for node in context.deployment.plan.nodes.itervalues():
        if node.template_name == node_template.name:
            current_instances += 1
    
    relationships = []
    for requirement in node_template.requirements:
        if requirement.relationship_template is not None:
            relationships.append(convert_relationship_template(context, requirement))

    plugins = context.presentation.service_template.plugins
    plugins = [convert_plugin(context, value) for value in plugins.itervalues()] if plugins is not None else []

    node_template = OrderedDict((
        ('name', node_template.name),
        ('id', node_template.name),
        ('type', node_type.name),
        ('properties', convert_properties(context, node_template.properties)),
        ('operations', convert_interfaces(context, node_template.interfaces)),
        ('type_hierarchy', convert_type_hierarchy(context, node_type, context.deployment.node_types)),
        ('relationships', relationships),
        ('plugins', plugins),
        ('capabilities', OrderedDict((
            ('scalable', OrderedDict((
                ('properties', OrderedDict((
                    ('current_instances', current_instances),
                    ('default_instances', node_template.default_instances),
                    ('min_instances', node_template.min_instances),
                    ('max_instances', node_template.max_instances if node_template.max_instances is not None else -1)))),))),)))))
    if host_node_template is not None:
        node_template['host_id'] = host_node_template.name
    return node_template

def convert_group_template(context, group_template):
    return OrderedDict((
        ('members', group_template.member_node_template_names),))

def convert_relationship_template(context, requirement):
    relationship_template = requirement.relationship_template
    relationship_type = context.deployment.relationship_types.get_descendant(relationship_template.type_name)
    
    return OrderedDict((
        ('type', relationship_type.name),
        ('type_hierarchy', convert_type_hierarchy(context, relationship_type, context.deployment.relationship_types)),
        ('target_id', requirement.target_node_template_name),
        ('properties', convert_properties(context, relationship_template.properties)),
        ('source_interfaces', OrderedDict()), # TODO: ?
        ('target_interfaces', OrderedDict()), # TODO: ?
        ('source_operations', convert_interfaces(context, relationship_template.source_interfaces)), 
        ('target_operations', convert_interfaces(context, relationship_template.target_interfaces))))

def convert_node(context, node):
    host_node = find_host_node(context, node)
    groups = find_groups(context, node)

    return OrderedDict((
        ('id', node.id),
        ('name', node.template_name),
        ('host_id', host_node.id if host_node is not None else None),
        ('relationships', [convert_relationship(context, v) for v in node.relationships]),
        ('scaling_groups', [OrderedDict((('name', group.template_name),)) for group in groups])))

def convert_relationship(context, relationship):
    target_node = context.deployment.plan.nodes.get(relationship.target_node_id)
    
    return OrderedDict((
        ('type', relationship.type_name), # template_name?
        ('target_id', relationship.target_node_id),
        ('target_name', target_node.template_name)))

def convert_interfaces(context, interfaces):
    operations = OrderedDict()
    
    duplicate_operation_names = set()
    for interface_name, interface in interfaces.iteritems():
        for operation_name, operation in interface.operations.iteritems():
            operation = convert_operation(context, operation)
            operations['%s.%s' % (interface_name, operation_name)] = operation
            if operation_name not in operations:
                operations[operation_name] = operation
            else:
                duplicate_operation_names.add(operation_name)

    # If the short form is not unique, then we should not have it at all 
    for operation_name in duplicate_operation_names:
        del operations[operation_name]
            
    return operations

def convert_operation(context, operation, is_workflow=False):
    implementation = operation.implementation
    if (not implementation) or ('/' in implementation):
        # Explicit script
        plugin_name = None
        operation_name = implementation
        plugin_executor = None
    else:
        # plugin.operation
        plugin_name, operation_name = operation.implementation.split('.', 1)
        plugin = context.presentation.service_template.plugins.get(plugin_name) if context.presentation.service_template.plugins is not None else None
        plugin_executor = plugin.executor if plugin is not None else None

    operation_dict = OrderedDict((
        ('plugin', plugin_name),
        ('operation', operation_name),
        ('has_intrinsic_functions', has_intrinsic_functions(context, operation.inputs)),
        ('executor', operation.executor or plugin_executor),
        ('max_retries', operation.max_retries),
        ('retry_interval', operation.retry_interval)))
    if is_workflow:
        operation_dict['parameters'] = convert_parameters(context, operation.inputs)
    else:
        operation_dict['inputs'] = convert_inputs(context, operation.inputs)
    return operation_dict

def convert_plugin(context, plugin):
    return OrderedDict((
        ('name', plugin._name),
        ('distribution', plugin.distribution),
        ('distribution_release', plugin.distribution_release),
        ('distribution_version', plugin.distribution_version),
        ('executor', plugin.executor),
        ('install', plugin.install),
        ('install_arguments', plugin.install_arguments),
        ('package_name', plugin.package_name),
        ('package_version', plugin.package_version),
        ('source', plugin.source),
        ('supported_platform', plugin.supported_platform)))

def convert_relationship_type(context, relationship_type):
    return OrderedDict((
        ('name', relationship_type.name),
        ('properties', convert_properties(context, relationship_type.properties)),
        ('source_interfaces', convert_interfaces(context, relationship_type.source_interfaces)),
        ('target_interfaces', convert_interfaces(context, relationship_type.target_interfaces)),
        ('type_hierarchy', convert_type_hierarchy(context, relationship_type, context.deployment.relationship_types))))

def convert_properties(context, properties):
    return OrderedDict((
        (k, as_raw(v.value)) for k, v in properties.iteritems()))

def convert_inputs(context, inputs):
    return OrderedDict((
        (k, as_raw(v.value)) for k, v in inputs.iteritems()))

def convert_parameters(context, parameters):
    return OrderedDict((
        (key, convert_parameter(context, value)) for key, value in parameters.iteritems()))

def convert_parameter(context, parameter):
    return OrderedDict((
        ('type', parameter.type_name),
        ('default', as_raw(parameter.value)),))

def convert_type_hierarchy(context, the_type, hierarchy):
    type_hierarchy = []
    while (the_type is not None) and (the_type.name is not None):
        type_hierarchy.insert(0, the_type.name)
        the_type = hierarchy.get_parent(the_type.name)
    return type_hierarchy

#
# Utils
#

def as_raw(value):
    if hasattr(value, 'as_raw'):
        value = value.as_raw
    elif isinstance(value, list):
        value = deepclone(value)
        for i in range(len(value)):
            value[i] = as_raw(value[i])
    elif isinstance(value, dict):
        value = deepclone(value)
        for k, v in value.iteritems():
            value[k] = as_raw(v)
    return value

def has_intrinsic_functions(context, value):
    if isinstance(value, Parameter):
        value = value.value

    if isinstance(value, Function):
        return True
    elif isinstance(value, dict):
        for v in value.itervalues():
            if has_intrinsic_functions(context, v):
                return True
    elif isinstance(value, list):
        for v in value:
            if has_intrinsic_functions(context, v):
                return True
    return False

def find_host_node_template(context, node_template):
    if context.deployment.node_types.is_descendant('cloudify.nodes.Compute', node_template.type_name):
        return node_template
    
    for requirement in node_template.requirements:
        relationship_template = requirement.relationship_template
        if relationship_template is not None:
            if context.deployment.relationship_types.is_descendant('cloudify.relationships.contained_in', relationship_template.type_name):
                return find_host_node_template(context, context.deployment.template.node_templates.get(requirement.target_node_template_name))

    return None

def find_host_node(context, node):
    node_template = context.deployment.template.node_templates.get(node.template_name)
    if context.deployment.node_types.is_descendant('cloudify.nodes.Compute', node_template.type_name):
        return node
    
    for relationship in node.relationships:
        if context.deployment.relationship_types.is_descendant('cloudify.relationships.contained_in', relationship.type_name):
            return find_host_node(context, context.deployment.plan.nodes.get(relationship.target_node_id))

    return None

def find_groups(context, node):
    groups = []
    for group in context.deployment.plan.groups.itervalues():
        if node.id in group.member_node_ids:
            groups.append(group)
    return groups
