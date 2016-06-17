
from .. import Consumer, BadImplementationError
from ..style import Style
from .code_generator import CodeGenerator, CodeMethod, CodeProperty, CodeAssignment, CodeNodeTemplate, CodeRelationship
from .context import Context
from inspect import getargspec
import sys

class Implementer(Consumer):
    """
    ARIA implementer.
    
    Creates Python classes for the presentation.
    """

    def __init__(self, presentation, args=[], root='out', style=Style()):
        super(Implementer, self).__init__(presentation, args)
        self.root = root
        self.style = style

    def consume(self):
        self.generate()
        self.service.context.dump()
    
    @property
    def service(self):
        """
        Gets the implemented service instance.
        
        For this to work, the service source code must have been generated. The Python
        runtime will then load this code by compiling it.
        """
        sys.path.append(self.root)
        try:
            from service import Service
            args = len(getargspec(Service.__init__).args) - 2
        except Exception as e:
            raise BadImplementationError('service code could not be compiled', e)
        try:
            context = Context(self.style)
            service = Service(context, *([None] * args))
            return service
        except Exception as e:
            raise BadImplementationError('Service class could not be instantiated', e)

    def generate(self):
        service_template = self.presentation.service_template
        
        generator = CodeGenerator()
        
        generator.description = service_template.description
        
        if service_template.node_types:
            for name, node_type in service_template.node_types.iteritems():
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

        if service_template.relationships:
            for name, relationship in service_template.relationships.iteritems():
                cls = generator.get_class(name)
                if relationship.derived_from:
                    cls.base = relationship.derived_from
                if relationship.description:
                    cls.description = relationship.description
                if relationship.properties:
                    for name, p in relationship.properties.iteritems():
                        cls.properties[name] = CodeProperty(generator, name, p.description, p.type, p.default)

        if service_template.inputs:
            for name, input in service_template.inputs.iteritems():
                generator.inputs[name] = CodeProperty(generator, name, input.description, input.type, input.default)

        if service_template.outputs:
            for name, output in service_template.outputs.iteritems():
                generator.outputs[name] = CodeAssignment(generator, name, output.description, output.value)
        
        if service_template.node_templates:
            for name, node_template in service_template.node_templates.iteritems():
                n = CodeNodeTemplate(generator, name, node_template.type, node_template.description)
                generator.nodes[name] = n
                if node_template.properties:
                    for name, p in node_template.properties.iteritems():
                        n.assignments[name] = p.value
                if node_template.relationships:
                    for r in node_template.relationships:
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
