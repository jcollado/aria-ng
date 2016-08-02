from clint.textui import puts

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
