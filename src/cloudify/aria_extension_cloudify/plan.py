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
from aria.utils import JSONValueEncoder, deepclone
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
    return OrderedDict((
        ('nodes', [convert_node_template(context, v, plan) for v in template.node_templates.itervalues()]),
        ('node_instances', [convert_node(context, v) for v in plan.nodes.itervalues()]),
        ('workflows', {})))

def convert_node_template(context, node_template, plan):
    node_type = context.deployment.node_types.get_descendant(node_template.type_name)
    
    current_instances = 0
    for node in plan.nodes.itervalues():
        if node.template_name == node_template.name:
            current_instances += 1
    
    relationships = []
    for requirement in node_template.requirements:
        if requirement.relationship_template is not None:
            relationships.append(convert_relationship_template(context, requirement.relationship_template))
    
    return OrderedDict((
        ('id', node_template.name),
        ('properties', deepclone(node_template.properties)),
        ('operations', convert_interfaces(context, node_template.interfaces)),
        ('type_hierarchy', []), # strings
        ('relationships', relationships),
        ('plugins', []), # strings
        ('type', node_type.name), # string
        ('capabilities', OrderedDict((
            ('scalable', OrderedDict((
                ('properties', OrderedDict((
                    ('current_instances', current_instances),
                    ('default_instances', node_template.default_instances),
                    ('min_instances', node_template.min_instances),
                    ('max_instances', node_template.max_instances or -1)))),))),)))))

def convert_relationship_template(context, relationship_template):
    return OrderedDict((
        ('target_id', relationship_template.template_name),
        ('source_operations', convert_interfaces(context, relationship_template.source_interfaces)), 
        ('target_operations', convert_interfaces(context, relationship_template.target_interfaces)),
        ('source_interfaces', OrderedDict()),
        ('target_interfaces', OrderedDict()),
        ('type_hierarchy', []), # strings
        ('properties', deepclone(relationship_template.properties))))

def convert_node(context, node):
    return OrderedDict((
        ('name', node.template_name), # string
        ('id', node.id), # unique string
        ('relationships', [convert_relationship(context, v) for v in node.relationships])))

def convert_relationship(context, relationship):
    return OrderedDict((
        ('type', relationship.template_name),
        ('target_name', relationship.target_node_id),
        ('target_id', relationship.target_node_id)))

def convert_interfaces(context, interfaces):
    operations = OrderedDict()
    for interface_name, interface in interfaces.iteritems():
        for operation_name, operation in interface.operations.iteritems():
            operation_name = '%s.%s' % (interface_name, operation_name)
            operations[operation_name] = convert_operation(context, operation)
    return operations

def convert_operation(context, operation):
    plugin_name, operation_name = operation.implementation.split('.', 1)
    return OrderedDict((
        ('plugin', plugin_name),
        ('operation', operation_name),
        ('parameters', OrderedDict()),
        ('has_intrinsic_functions', False),
        ('executor', None),
        ('inputs', deepclone(operation.inputs)),
        ('max_retries', 1),
        ('retry_interval', 1)))
