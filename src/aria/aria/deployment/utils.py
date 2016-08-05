from clint.textui import puts

def instantiate_value(context, value):
    if hasattr(value, 'evaluate'):
        value = value.evaluate(context)
    return value

def instantiate_properties(context, properties, from_properties):
    if not from_properties:
        return
    for property_name, value in from_properties.iteritems():
        properties[property_name] = instantiate_value(context, value)

def instantiate_interfaces(context, interfaces, from_interfaces):
    if not from_interfaces:
        return
    for interface_name, interface in from_interfaces.iteritems():
        interfaces[interface_name] = interface.instantiate(context)

def dump_properties(context, properties, name='Properties'):
    if not properties:
        return
    with context.style.indent:
        puts('%s:' % name)
        with context.style.indent:
            for property_name, value in properties.iteritems():
                puts('%s = %s' % (context.style.property(property_name), context.style.literal(value)))

def dump_interfaces(context, interfaces):
    if not interfaces:
        return
    with context.style.indent:
        puts('Interfaces:')
        with context.style.indent:
            for interface in interfaces.itervalues():
                interface.dump(context)
