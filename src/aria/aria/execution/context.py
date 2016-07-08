
from .. import classname
from .exceptions import ExecutorNotFoundError
from .cloudify import HostAgentExecutor, CentralDeploymentAgentExecutor
from clint.textui import puts

class Relationship(object):
    def __init__(self, source, relationship, target):
        self.source = source
        self.relationship = relationship
        self.target = target

class ExecutionContext(object):
    """
    Service execution context.
    """
    def __init__(self, style):
        self.service = None
        self.relationships = []
        self.style = style
        self.executors = {}
        self.executors['host_agent'] = HostAgentExecutor()
        self.executors['central_deployment_agent'] = CentralDeploymentAgentExecutor()
    
    def relate(self, source, relationship, target):
        """
        Creates the graph.
        """
        self.relationships.append(Relationship(source, relationship, target))
        
    def executor(self, name):
        if name not in self.executors:
            raise ExecutorNotFoundError(name)
        return self.executors[name]
    
    def get_relationship_from(self, source):
        relationships = []
        for relationship in self.relationships:
            if relationship.source == source:
                relationships.append(relationship)
        return relationships
    
    def get_node_name(self, node):
        for name in self.nodes:
            the_node = getattr(self.service, name)
            if node == the_node:
                return name
        return None
    
    @property
    def inputs(self):
        return self.service.__class__.INPUTS if hasattr(self.service.__class__, 'INPUTS') else []

    @property
    def outputs(self):
        return self.service.__class__.OUTPUTS if hasattr(self.service.__class__, 'OUTPUTS') else []
    
    @property
    def nodes(self):
        return self.service.__class__.NODES if hasattr(self.service.__class__, 'NODES') else []

    @property
    def workflows(self):
        return self.service.__class__.WORKFLOWS if hasattr(self.service.__class__, 'WORKFLOWS') else []
    
    def dump(self):
        if self.inputs:
            puts(self.style.section('Inputs:'))
            with self.style.indent:
                for name in self.inputs:
                    puts('%s' % self.style.property(name))
        if self.outputs:
            puts(self.style.section('Outputs:'))
            with self.style.indent:
                for name in self.outputs:
                    prop = getattr(self.service.__class__, name)
                    puts('%s: %s' % (self.style.property(name), prop.__doc__.strip()))
        if self.nodes:
            puts(self.style.section('Topology:'))
            with self.style.indent:
                for name in self.nodes:
                    node = getattr(self.service, name)
                    puts('%s: %s' % (self.style.node(name), self.style.type(classname(node))))
                    relationships = self.get_relationship_from(node)
                    if relationships:
                        with self.style.indent:
                            for relationship in relationships:
                                puts('-> %s %s' % (self.style.type(classname(relationship.relationship)), self.style.node(self.get_node_name(relationship.target))))
