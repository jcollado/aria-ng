
#from aria.consumer import Implementer

def prepare_deployment_plan(plan, inputs=None, **kwargs):
    """
    Prepare a plan for deployment
    """
    print '!!! prepare_deployment_plan'
    print plan
    print inputs
    print kwargs
    
    #implementer = Implementer(plan)
    #implementer.implement()
    #service = implementer.service
    #node_instances = [create_node_instance(name, getattr(service, name)) for name in service.context.nodes]
    
    return DeploymentPlan(plan).plan

class DeploymentPlan(object):
    def __init__(self, presentation):
        self.presentation = presentation
        self.plugins = [self.create_plugin(name, p) for name, p in self.presentation.service_template.plugins.iteritems()]

    @property
    def plan(self):
        nodes = [self.create_node(name, n) for name, n in self.presentation.service_template.node_templates.iteritems()]
        node_instances = [self.create_node_instance(name, n) for name, n in self.presentation.service_template.node_templates.iteritems()]
        workflows = {name: self.create_operation(o) for name, o in self.presentation.service_template.workflows.iteritems()}
        
        return {
            'nodes': nodes,
            'node_instances': node_instances,
            'workflows': workflows}

    def get_node_type(self, node_template):
        return self.presentation.service_template.node_types[node_template]

    def append_from_type(self, r, node_type_name):
        r['type_hierarchy'].insert(0, node_type_name)
        node_type = self.get_node_type(node_type_name)
        if node_type.properties:
            for property_name, p in node_type.properties.iteritems():
                if p.default is not None:
                    r['properties'][property_name] = p.default
        if node_type.interfaces:
            for interface_name, i in node_type.interfaces.iteritems():
                for operation_name, o in i.operations.iteritems():
                    # Some tests seem to expect the first format, some the latter
                    r['operations']['%s.%s' % (interface_name, operation_name)] = self.create_operation(o)
                    if not operation_name in r['operations']:
                        r['operations'][operation_name] = self.create_operation(o)
        if node_type.derived_from:
            self.append_from_type(r, node_type.derived_from)

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
        self.append_from_type(r, node_template.type)
        if node_template.properties:
            for property_name, p in node_template.properties.iteritems():
                r['properties'][property_name] = p.value
        #r['relationships'] =
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
        node_instance['id'] = name
        #node_instance['node_id'] = name
        #node_instance['relationships'] = []
        #node_instance['host_id'] =
        #node_instance['deployment_id'] =
        #node_instance['runtime_properties'] = {}
        #node_instance['state'] =
        #node_instance['version'] =
        return node_instance

    def create_operation(self, operation):
        r = {}
        implementation = operation.mapping or operation.implementation
        plugin, command = implementation.split('.', 1)
        r['plugin'] = plugin
        r['operation'] = command
        r['parameters'] = {}
        r['parameters']['nodes'] = [] #['node1']
        r['parameters']['testing'] = '' #'download_resource'
        r['parameters']['operation'] = '' #'download_template'
        r['has_intrinsic_functions'] = False
        r['executor'] = operation.executor
        r['max_retries'] = 0 #-1
        r['retry_interval'] = None #30
        return r

    def create_plugin(self, name, plugin):
        r = {}
        r['name'] = name
        return r
