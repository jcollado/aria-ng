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
from aria.utils import JSONValueEncoder
from collections import OrderedDict
import json

class Plan(BasicPlan):
    """
    Emits the deployment plan instantiated from the deployment template.
    """

    def consume(self):
        classic_plan = self.create_classic_plan()
        if classic_plan is not None:
            print json.dumps(classic_plan, indent=2, cls=JSONValueEncoder)

    def create_classic_plan(self):
        self.create_deployment_plan()
        if (self.context.deployment.plan is not None) and (not self.context.validation.has_issues):
            return convert_plan(self.context, self.context.deployment.plan, self.context.deployment.template)
        return None

def convert_plan(context, plan, template):
    r = OrderedDict((
        ('description', plan.description),
        ('inputs', convert_properties(context, plan.inputs)),
        ('outputs', convert_properties(context, plan.outputs)),
        ('nodes', [convert_node_template(context, value, plan) for value in template.node_templates.itervalues()]),
        ('node_instances', [convert_node(context, v) for v in plan.nodes.itervalues()]),
        ('workflows', OrderedDict((
            key, convert_operation(context, value, True)) for key, value in plan.operations.iteritems())),
        ('relationships', OrderedDict((
            (relationship_type.name, convert_relationship_type(context, relationship_type)) for relationship_type in context.deployment.relationship_types.iter_descendants())))))

    #setattr(version, 'raw', version['raw'])
    #setattr(version, 'definitions_name', version['definitions_name'])
    #setattr(version, 'definitions_version', version['definitions_version'])
    
    #setattr(r, 'version', r['version'])
    setattr(r, 'inputs', r['inputs'])
    setattr(r, 'outputs', r['outputs'])
    setattr(r, 'node_templates', r['nodes'])
    
    return r

def convert_node_template(context, node_template, plan):
    node_type = context.deployment.node_types.get_descendant(node_template.type_name)
    
    current_instances = 0
    for node in plan.nodes.itervalues():
        if node.template_name == node_template.name:
            current_instances += 1
    
    relationships = []
    for requirement in node_template.requirements:
        if requirement.relationship_template is not None:
            relationships.append(convert_relationship_template(context, requirement))

    plugins = context.presentation.service_template.plugins
    plugins = [convert_plugin(context, value) for value in plugins.itervalues()] if plugins is not None else []

    return OrderedDict((
        ('id', node_template.name),
        ('name', node_template.name),
        ('properties', convert_properties(context, node_template.properties)),
        ('operations', convert_interfaces(context, node_template.interfaces)),
        ('type_hierarchy', convert_type_hierarchy(context, node_type, context.deployment.node_types)),
        ('relationships', relationships),
        ('plugins', plugins),
        ('type', node_type.name),
        ('capabilities', OrderedDict((
            ('scalable', OrderedDict((
                ('properties', OrderedDict((
                    ('current_instances', current_instances),
                    ('default_instances', node_template.default_instances),
                    ('min_instances', node_template.min_instances),
                    ('max_instances', node_template.max_instances or -1)))),))),)))))

def convert_relationship_type(context, relationship_type):
    return OrderedDict((
        ('name', relationship_type.name),
        ('properties', convert_properties(context, relationship_type.properties)),
        ('source_interfaces', convert_interfaces(context, relationship_type.source_interfaces)),
        ('target_interfaces', convert_interfaces(context, relationship_type.target_interfaces)),
        ('type_hierarchy', convert_type_hierarchy(context, relationship_type, context.deployment.relationship_types))))

def convert_relationship_template(context, requirement):
    relationship_template = requirement.relationship_template
    relationship_type = context.deployment.relationship_types.get_descendant(relationship_template.type_name)
    
    return OrderedDict((
        ('type', relationship_type.name),
        ('target_id', requirement.target_node_template_name),
        ('source_operations', convert_interfaces(context, relationship_template.source_interfaces)), 
        ('target_operations', convert_interfaces(context, relationship_template.target_interfaces)),
        ('source_interfaces', OrderedDict()), # TODO: ?
        ('target_interfaces', OrderedDict()), # TODO: ?
        ('type_hierarchy', convert_type_hierarchy(context, relationship_type, context.deployment.relationship_types)),
        ('properties', convert_properties(context, relationship_template.properties))))

def convert_node(context, node):
    host_node = find_host_node(context, node)

    return OrderedDict((
        ('name', node.template_name),
        ('id', node.id),
        ('relationships', [convert_relationship(context, v) for v in node.relationships]),
        ('host_id', host_node.id if host_node is not None else None)))

def convert_relationship(context, relationship):
    target_node = context.deployment.plan.nodes.get(relationship.target_node_id)
    
    return OrderedDict((
        ('type', relationship.type_name), # template_name?
        ('target_name', target_node.template_name),
        ('target_id', relationship.target_node_id)))

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

    return OrderedDict((
        ('plugin', plugin_name),
        ('operation', operation_name),
        ('has_intrinsic_functions', False), # TODO
        ('executor', operation.executor or plugin_executor),
        ('parameters' if is_workflow else 'inputs', convert_parameters(context, operation.inputs)),
        ('max_retries', operation.max_retries),
        ('retry_interval', operation.retry_interval)))

def convert_plugin(context, plugin):
    return OrderedDict((
        ('distribution', plugin.distribution),
        ('distribution_release', plugin.distribution_release),
        ('distribution_version', plugin.distribution_version),
        ('executor', plugin.executor),
        ('install', plugin.install),
        ('install_arguments', plugin.install_arguments),
        ('name', plugin._name),
        ('package_name', plugin.package_name),
        ('package_version', plugin.package_version),
        ('source', plugin.source),
        ('supported_platform', plugin.supported_platform)))

def convert_properties(context, properties):
    return OrderedDict((
        (k, v.value) for k, v in properties.iteritems()))

def convert_parameters(context, parameters):
    return OrderedDict((
        (key, convert_parameter(context, value)) for key, value in parameters.iteritems()))

def convert_parameter(context, parameter):
    return OrderedDict((
        ('type', parameter.type_name),
        ('default', parameter.value),))

def convert_type_hierarchy(context, the_type, hierarchy):
    type_hierarchy = []
    while (the_type is not None) and (the_type.name is not None):
        type_hierarchy.insert(0, the_type.name)
        the_type = hierarchy.get_parent(the_type.name)
    return type_hierarchy

def find_host_node(context, node):
    for relationship in node.relationships:
        if context.deployment.relationship_types.is_descendant('cloudify.relationships.contained_in', relationship.type_name):
            target_node = context.deployment.plan.nodes.get(relationship.target_node_id)
            if target_node is not None:
                next_target_node = find_host_node(context, target_node)
                if next_target_node is not None:
                    target_node = next_target_node
            return target_node
