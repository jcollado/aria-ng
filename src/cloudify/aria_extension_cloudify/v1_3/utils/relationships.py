
from .properties import get_inherited_property_definitions, get_assigned_and_defined_property_values
from aria import Issue

#
# RelationshipType
#

def get_relationship_inherited_property_definitions(context, presentation):
    properties = get_inherited_property_definitions(context, presentation, 'properties')
    
    for key in properties.iterkeys():
        if key != 'connection_type':
            context.validation.report('relationship type "%s" has unsupported property: %s' % (presentation._fullname, repr(key)), locator=presentation._get_grandchild_locator('properties', key), level=Issue.BETWEEN_FIELDS)
    
    definition = properties.get('connection_type')
    if definition is not None:
        default = definition.default
        if default not in ('all_to_all', 'all_to_one'):
            context.validation.report('"connection_type" property default is not "all_to_all" or "all_to_one" in relationship type "%s": %s' % (presentation._fullname, repr(default)), locator=definition._locator, level=Issue.BETWEEN_FIELDS)
    
    return properties

#
# RelationshipTemplate
#

def get_relationship_assigned_and_defined_property_values(context, presentation):
    values = get_assigned_and_defined_property_values(context, presentation)

    value = values.get('connection_type', 'all_to_all')
    if value not in ('all_to_all', 'all_to_one'):
        context.validation.report('"connection_type" property is not "all_to_all" or "all_to_one" in relationship in node template "%s": %s' % (presentation._container._fullname, repr(value)), locator=presentation._get_grandchild_locator('properties', 'connection_type'), level=Issue.BETWEEN_FIELDS)
    values['connection_type'] = value
    
    return values