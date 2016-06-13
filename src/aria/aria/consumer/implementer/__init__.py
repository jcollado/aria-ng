
from aria import make_agnostic
from aria.consumer import Consumer
from code_generator import CodeGenerator, CodeMethod, CodeProperty, CodeAssignment, CodeNodeTemplate, CodeRelationship
import sys, inspect

class Context(object):
    """
    Fake blueprint context used for validation.
    """
    def __init__(self):
        self.profile = None
    
    def relate(self, source, relationship, target):
        """
        A real context would build a node graph here.
        """
        pass

class Implementer(Consumer):
    """
    ARIA implementer.
    
    Creates Python classes for the presentation.
    """

    def __init__(self, presentation, args=[], root='out'):
        super(Implementer, self).__init__(presentation, args)
        self.root = root

    def consume(self):
        self.generate()
        print self.blueprint
    
    @property
    def blueprint(self):
        """
        Gets the implemented blueprint instance.
        
        For this to work, the blueprint source code must have been generated. The Python
        runtime will then load this code by compiling it.
        """
        sys.path.append(self.root)
        from blueprint import Blueprint
        args = len(inspect.getargspec(Blueprint.__init__).args) - 2
        context = Context()
        blueprint = Blueprint(context, *([None] * args))
        return blueprint

    def generate(self):
        profile = self.presentation.profile
        
        generator = CodeGenerator()
        
        generator.description = profile.description
        
        if profile.node_types:
            for name, node_type in profile.node_types.iteritems():
                cls = generator.get_class(name)
                if node_type.derived_from:
                    cls.base = node_type.derived_from
                if node_type.description:
                    cls.description = node_type.description
                if node_type.properties:
                    for name, p in node_type.properties.iteritems():
                        cls.properties[name] = CodeProperty(generator, name, p.description, p.type, p.default)
                if node_type.interfaces:
                    for name, i in node_type.interfaces.iteritems():
                        for wname, w in i.workflows.iteritems():
                            method = CodeMethod(generator, wname, name, w.implementation, w.executor)
                            cls.methods[wname] = method
                            if w.inputs:
                                for pname, p in w.inputs.iteritems():
                                    method.arguments[pname] = CodeProperty(generator, pname, p.description, p.type, p.default)

        if profile.relationships:
            for name, relationship in profile.relationships.iteritems():
                cls = generator.get_class(name)
                if relationship.derived_from:
                    cls.base = relationship.derived_from
                if relationship.description:
                    cls.description = relationship.description
                if relationship.properties:
                    for name, p in relationship.properties.iteritems():
                        cls.properties[name] = CodeProperty(generator, name, p.description, p.type, p.default)

        if profile.inputs:
            for name, input in profile.inputs.iteritems():
                generator.inputs[name] = CodeProperty(generator, name, input.description, input.type, input.default)

        if profile.outputs:
            for name, output in profile.outputs.iteritems():
                generator.outputs[name] = CodeAssignment(generator, name, output.description, output.value)
        
        if profile.node_templates:
            for name, node in profile.node_templates.iteritems():
                n = CodeNodeTemplate(generator, name, node.type, node.description)
                generator.nodes[name] = n
                if node.properties:
                    for name, p in node.properties.iteritems():
                        n.assignments[name] = p.value
                if node.relationships:
                    for r in node.relationships:
                        n.relationships.append(CodeRelationship(generator, r.type, r.target))
        
        generator.write(self.root)
        
        return generator

    def dump(self):
        generator = self.implement()
        for m in generator.module.modules:
            if m.name:
                puts(colored.red(m.file))
            with indent(2):
                for c in m.classes.itervalues():
                    puts(str(c))
