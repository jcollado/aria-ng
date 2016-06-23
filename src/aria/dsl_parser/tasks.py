
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

GENERATED_IDS = set()

def generate_id():
    # TODO: a dumb way to make sure our IDs are unique, but better than nothing
    def gen():
        return '%05x' % random.randrange(16 ** 5)
    id = gen()
    while id in GENERATED_IDS:
        id = gen()
    GENERATED_IDS.add(id)
    return id
    
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

        self.relate_node_instances()
        
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

    def get_relationship(self, name):
        return self.presentation.service_template.relationships[name]
    
    def get_node_instances(self, name):
        node_instances = []
        for node_instance in self.node_instances:
            if node_instance['name'] == name:
                node_instances.append(node_instance)
        return node_instances
    
    def is_contained_relationship(self, type):
        if type == 'cloudify.relationships.contained_in':
            return True
        relationship = self.get_relationship(type)
        if relationship.derived_from:
            return self.is_contained_relationship(relationship.derived_from)
        return False
    
    def relate_node_instances(self):
        for node_instance in self.node_instances:
            node_template = self.get_node_template(node_instance['name'])
            if node_template.relationships:
                relationships = []
                for relationship in node_template.relationships:
                    if self.is_contained_relationship(relationship.type):
                        node_instance['host_id'] = target['id']
                    targets = self.get_node_instances(relationship.target)
                    for target in targets:
                        r = {}
                        r['type'] = relationship.type
                        r['target_name'] = relationship.target
                        r['target_id'] = target['id']
                        relationships.append(r)
                node_instance['relationships'] = relationships

    def append_properties(self, r, properties):
        if properties:
            for name, p in properties.iteritems():
                r[name] = {}
                r[name]['default'] = p.default
    
    def append_property_values(self, r, properties):
        if properties:
            for name, p in properties.iteritems():
                r[name] = p.value

    def append_operations_from_interfaces(self, r, interfaces):
        if interfaces:
            for interface_name, i in interfaces.iteritems():
                for operation_name, o in i.operations.iteritems():
                    # Seems we need to support both long and short lookup styles?
                    operation = self.create_operation(operation_name, o)
                    r['%s.%s' % (interface_name, operation_name)] = operation
                    r[operation_name] = operation

    def append_from_node_type(self, r, node_type_name):
        r['type_hierarchy'].insert(0, node_type_name)
        node_type = self.get_node_type(node_type_name)
        if node_type.derived_from:
            self.append_from_node_type(r, node_type.derived_from)
        if node_type.properties:
            for property_name, p in node_type.properties.iteritems():
                if p.default is not None:
                    r['properties'][property_name] = p.default
        self.append_operations_from_interfaces(r['operations'], node_type.interfaces)
    
    def append_interfaces(self, r, interfaces):
        # Is this actually used by dsl_parser consumers?
        if interfaces:
            for interface_name, i in interfaces.iteritems():
                r[interface_name] = {}
                for operation_name, o in i.operations.iteritems():
                    r[interface_name][operation_name] = {}
                    r[interface_name][operation_name]['implementation'] = o.implementation
                    r[interface_name][operation_name]['inputs'] = {} # TODO: o.inputs
                    r[interface_name][operation_name]['max_retries'] = o.max_retries
                    r[interface_name][operation_name]['retry_interval'] = o.retry_interval
                    r[interface_name][operation_name]['executor'] = o.executor

    def append_from_relationship_type(self, r, type):
        r['type_hierarchy'].insert(0, type)
        relationship_type = self.get_relationship(type)
        if relationship_type.properties:
            for property_name, p in relationship_type.properties.iteritems():
                if p.default is not None:
                    r['properties'][property_name] = p.default
        if relationship_type.derived_from:
            self.append_from_relationship_type(r, relationship_type.derived_from)
        self.append_operations_from_interfaces(r['source_operations'], relationship_type.source_interfaces)
        self.append_operations_from_interfaces(r['target_operations'], relationship_type.target_interfaces)
        self.append_interfaces(r['source_interfaces'], relationship_type.source_interfaces)
        self.append_interfaces(r['target_interfaces'], relationship_type.target_interfaces)

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
        self.append_property_values(r['properties'], node_template.properties)
        r['relationships'] = []
        if node_template.relationships:
            for relationship in node_template.relationships:
                rr = {}
                rr['target_id'] = relationship.target
                rr['source_operations'] = {}
                rr['target_operations'] = {}
                rr['source_interfaces'] = {}
                rr['target_interfaces'] = {}
                rr['type_hierarchy'] = []
                rr['properties'] = {}
                self.append_from_relationship_type(rr, relationship.type)
                self.append_property_values(rr['properties'], relationship.properties)
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
        r['plugin'] = plugin
        r['operation'] = command
        r['parameters'] = {}
        self.append_properties(r['parameters'], operation.parameters)
        r['has_intrinsic_functions'] = False
        r['executor'] = operation.executor
        #if not r['executor'] and plugin:
        #    r['executor'] = self.presentation.service_template.plugins[plugin].executor
        r['inputs'] = {}
        self.append_properties(r['inputs'], operation.inputs)
        r['max_retries'] = operation.max_retries if operation.max_retries is not None else 1
        r['retry_interval'] = operation.retry_interval if operation.retry_interval is not None else 1
        # Note: the default 1s are required for TestExecuteOperationWorkflow.test_execute_operation_with_dependency_order
        return r

    def create_plugin(self, name, plugin):
        r = {}
        r['name'] = name
        return r
