
from .. import InvalidValueError
from clint.textui import puts
from collections import OrderedDict

def instantiate_value(context, container, value):
    if isinstance(value, list):
        return [instantiate_value(context, container, v) for v in value]
    elif isinstance(value, dict):
        return OrderedDict((k, instantiate_value(context, container, v)) for k, v in value.iteritems())
    elif hasattr(value, '_evaluate'):
        value = value._evaluate(context, container)
        value = instantiate_value(context, container, value)
    return value

def instantiate_properties(context, container, properties, from_properties):
    if not from_properties:
        return
    for property_name, value in from_properties.iteritems():
        try:
            properties[property_name] = instantiate_value(context, container, value)
        except InvalidValueError as e:
            context.validation.report(issue=e.issue)

def instantiate_interfaces(context, container, interfaces, from_interfaces):
    if not from_interfaces:
        return
    for interface_name, interface in from_interfaces.iteritems():
        interfaces[interface_name] = interface.instantiate(context, container)

def dump_properties(context, properties, name='Properties'):
    if not properties:
        return
    puts('%s:' % name)
    with context.style.indent:
        for property_name, value in properties.iteritems():
            puts('%s = %s' % (context.style.property(property_name), context.style.literal(value)))

def dump_interfaces(context, interfaces):
    if not interfaces:
        return
    puts('Interfaces:')
    with context.style.indent:
        for interface in interfaces.itervalues():
            interface.dump(context)
