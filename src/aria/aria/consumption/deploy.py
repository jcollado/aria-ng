
from .consumer import Consumer
from clint.textui import puts, colored, indent

class Deploy(Consumer):
    """
    ARIA deployer.
    
    Created a deployment plan for the presentation.
    """

    def consume(self):
        if self.context.presentation.node_templates:
            for node_template_name, node_template in self.context.presentation.node_templates.iteritems():
                puts('Node template: %s' % node_template_name)
                requirements = node_template._get_requirements(self.context)
                if requirements:
                    with indent(2):
                        puts('Requirements:')
                        with indent(2):
                            for requirement_name, requirement in requirements:
                                puts('Requirement name: %s' % requirement_name)
                                with indent(2):
                                    node, node_variant = requirement._get_node(self.context)
                                    if node is not None:
                                        if node_variant == 'node_type':
                                            puts('Node type: %s' % node._name)
                                        else:
                                            puts('Node template: %s' % node._name)
                                            
                                    capability, capability_variant = requirement._get_capability(self.context)
                                    if capability is not None:
                                        capability_type = capability
                                        if capability_variant == 'capability_type':
                                            puts('Capability type: %s' % capability_type._name)
                                        else:
                                            capability_type = capability._get_type(self.context)
                                            puts('Capability name: %s (type: %s)' % (capability._name, capability_type._name))
                                    
                                    relationship = requirement.relationship
                                    if relationship is not None:
                                        relationship_type = relationship._get_type(self.context) # RelationshipType or RelationshipTemplate
                                        
                                        puts('Relationship type: %s' % relationship_type._name)
                                    
                                        properties = relationship._get_properties(self.context)
                                        if properties:
                                            with indent(2):
                                                puts('Properties:')
                                                with indent(2):
                                                    for property_name, prop in properties.iteritems():
                                                        puts('%s = %s' % (property_name, prop))
