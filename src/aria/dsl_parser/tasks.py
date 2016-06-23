
#from aria.consumer import Implementer

import random

def prepare_deployment_plan(plan, inputs=None, **kwargs):
    """
    Prepare a plan for deployment
    """
    #print '!!! prepare_deployment_plan'
    #print plan
    #print inputs
    #print kwargs
    
    #implementer = Implementer(plan)
    #implementer.implement()
    #service = implementer.service
    #node_instances = [create_node_instance(name, getattr(service, name)) for name in service.context.nodes]
    
    return DeploymentPlan(plan).plan

def generate_id():
    """
    This is not guaranteed to be unique!!!
    """
    return '%05x' % random.randrange(16 ** 5)
    
class DeploymentPlan(object):
    def __init__(self, presentation):
        self.presentation = presentation
        
        self.plugins = [self.create_plugin(name, p) for name, p in self.presentation.service_template.plugins.iteritems()] if self.presentation.service_template.plugins else []
        
        self.nodes = [self.create_node(name, n) for name, n in self.presentation.service_template.node_templates.iteritems()] if self.presentation.service_template.node_templates else []

        self.node_instances = []
        if self.presentation.service_template.node_templates:
            for name, node_template in self.presentation.service_template.node_templates.iteritems():
                count = node_template.instances.deploy if (node_template.instances and node_template.instances.deploy is not None) else 1
                for _ in range(count):
                    node_instance = self.create_node_instance(name, node_template)
                    self.node_instances.append(node_instance)

        self.relate()
        
        self.workflows = {name: self.create_operation(name, o) for name, o in self.presentation.service_template.workflows.iteritems()} if self.presentation.service_template.workflows else {}

    @property
    def plan(self):
        return {
            'nodes': self.nodes,
            'node_instances': self.node_instances,
            'workflows': self.workflows}

    def get_node_type(self, name):
        return self.presentation.service_template.node_types[name]

    def get_node_template(self, name):
        return self.presentation.service_template.node_templates[name]
    
    def get_node_instances(self, name):
        node_instances = []
        for node_instance in self.node_instances:
            if node_instance['name'] == name:
                node_instances.append(node_instance)
        return node_instances
        
    def relate(self):
        for node_instance in self.node_instances:
            node_template = self.get_node_template(node_instance['name'])
            if node_template.relationships:
                relationships = []
                for relationship in node_template.relationships:
                    targets = self.get_node_instances(relationship.target)
                    for target in targets:
                        r = {}
                        r['target_name'] = relationship.target
                        r['target_id'] = target['id']
                        relationships.append(r)
                node_instance['relationships'] = relationships

    def append_from_node_type(self, r, node_type_name):
        r['type_hierarchy'].insert(0, node_type_name)
        node_type = self.get_node_type(node_type_name)
        if node_type.derived_from:
            self.append_from_node_type(r, node_type.derived_from)
        if node_type.properties:
            for property_name, p in node_type.properties.iteritems():
                if p.default is not None:
                    r['properties'][property_name] = p.default
        if node_type.interfaces:
            for interface_name, i in node_type.interfaces.iteritems():
                for operation_name, o in i.operations.iteritems():
                    # Sometimes we expect the first format, sometimes the latter
                    operation = self.create_operation(operation_name, o)
                    r['operations']['%s.%s' % (interface_name, operation_name)] = operation
                    if operation_name not in r['operations']:
                        r['operations'][operation_name] = operation

    def create_node(self, name, node_template):
        r = {}
        r['capabilities'] = {}
        r['capabilities']['scalable'] = {}
        r['capabilities']['scalable']['properties'] = {}
        r['capabilities']['scalable']['properties']['current_instances'] = None
        r['capabilities']['scalable']['properties']['default_instances'] = None
        r['capabilities']['scalable']['properties']['min_instances'] = None
        r['capabilities']['scalable']['properties']['max_instances'] = None
        # See: cloudify_rest_client/nodes.py
        r['id'] = name
        #r['deployment_id'] =
        r['properties'] = {}
        r['operations'] = {}
        r['type_hierarchy'] = []
        self.append_from_node_type(r, node_template.type)
        if node_template.properties:
            for property_name, p in node_template.properties.iteritems():
                r['properties'][property_name] = p.value
        r['relationships'] = []
        if node_template.relationships:
            for relationship in node_template.relationships:
                rr = {}
                rr['target_id'] = relationship.target
                #rr['source_operations'] = {}
                #rr['target_operations'] = {}
                rr['type_hierarchy'] = [relationship.type] # TODO: inherit
                r['relationships'].append(rr)
        #r['blueprint_id'] =
        r['plugins'] = self.plugins
        #r['number_of_instances'] =
        #r['planned_number_of_instances'] =
        #r['deploy_number_of_instances'] =
        #r['host_id'] =
        r['type'] = node_template.type
        return r

    def create_node_instance(self, name, node_template):
        node_instance = {}
        node_instance['name'] = name
        # See: cloudify_rest_client/node_instances.py
        id = generate_id()
        node_instance['id'] = '%s_%s' % (name, id)
        #node_instance['node_id'] = id
        #node_instance['relationships'] = []
        #node_instance['host_id'] = 
        #node_instance['deployment_id'] =
        #node_instance['runtime_properties'] = {}
        #node_instance['state'] =
        #node_instance['version'] =
        return node_instance

    def create_operation(self, name, operation):
        r = {}
        implementation = operation.mapping or operation.implementation
        plugin, command = implementation.split('.', 1) if implementation else (None, None)
        r['name'] = name
        r['plugin'] = plugin
        r['operation'] = command
        r['parameters'] = {}
        if operation.parameters:
            for name, p in operation.parameters.iteritems():
                r['parameters'][name] = {}
                r['parameters'][name]['default'] = p.default
        r['has_intrinsic_functions'] = False
        r['executor'] = operation.executor
        r['inputs'] = {}
        if operation.inputs:
            for name, i in operation.inputs.iteritems():
                r['inputs'][name] = {}
                r['inputs'][name]['default'] = i.default
        #if not r['executor'] and plugin:
        #    r['executor'] = self.presentation.service_template.plugins[plugin].executor
        r['max_retries'] = 1 #-1
        r['retry_interval'] = 1 #30
        return r

    def create_plugin(self, name, plugin):
        r = {}
        r['name'] = name
        return r
