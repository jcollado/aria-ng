
from .. import Issue, merge
from collections import OrderedDict
from copy import deepcopy

def coerce_property_value(context, presentation, name, prop, the_type, get_type_fn):
    value = getattr(prop, 'value', None)
    if (value is not None) and (the_type is not None) and (get_type_fn is not None):
        cls = get_type_fn(the_type)
        if cls is None:
            context.validation.report('"%s" is defined with an unsupported type in %s: %s' % (name, presentation._fullname, the_type), locator=prop._locator, level=Issue.FIELD)
        else:
            try:
                value = cls(value)
            except ValueError:
                context.validation.report('"%s" must be coercible to %s.%s in %s: %s' % (name, cls.__module__, cls.__name__, presentation._fullname, repr(value)), locator=prop._locator, level=Issue.FIELD)
    return value

def get_inherited_property_definitions(context, presentation, field_name, for_presentation=None):
    """
    Assumes that we have a \_get\_parent(context) method.
    """
    
    # Get definitions from parent
    parent = presentation._get_parent(context)
    definitions = get_inherited_property_definitions(context, parent, field_name, presentation) if parent is not None else OrderedDict()
    
    # Add/merge our definitions
    our_definitions = getattr(presentation, field_name)
    if our_definitions is not None:
        for name, our_definition in our_definitions.iteritems():
            if name in definitions:
                definition = definitions[name]
                
                # Check if we changed the type
                type1 = getattr(definition, 'type', None)
                type2 = getattr(our_definition, 'type', None)
                if type1 != type2:
                    context.validation.report('property override changes type from "%s" to "%s" for "%s" in %s' % (type1, type2, name, presentation._fullname), locator=presentation._get_grandchild_locator(field_name, name), level=Issue.BETWEEN_TYPES)
                
                merge(definition._raw, deepcopy(our_definition._raw))
            else:
                if for_presentation is not None:
                    definitions[name] = our_definition._clone(for_presentation)
                else:
                    definitions[name] = our_definition
        
    return definitions

def get_defined_property_values(context, presentation, type_name, assignments_field_name, definitions_fn_name, get_type_fn=None):
    """
    Assumes that we have a \_get\_type(context) method.
    """
    values = OrderedDict()
    
    the_type = presentation._get_type(context)
    assignments = getattr(presentation, assignments_field_name)
    definitions = getattr(the_type, definitions_fn_name)(context) if the_type is not None else None

    # Fill in our assignments, but make sure they are defined
    if assignments is not None:
        for name, assignment in assignments.iteritems():
            if (definitions is not None) and (name in definitions):
                definition = definitions[name]
                the_type = getattr(definition, 'type', None)
                
                # Coerce value
                value = coerce_property_value(context, presentation, name, assignment, the_type, get_type_fn)
                    
                values[name] = value
            else:
                context.validation.report('assignment to undefined %s "%s" in %s' % (type_name, name, presentation._fullname), locator=presentation._get_grandchild_locator(assignments_field_name, name), level=Issue.BETWEEN_TYPES)
    
    # Fill in defaults from the definitions, and check if required fields have not been assigned
    if definitions is not None:
        for name, definition in definitions.iteritems():
            if (values.get(name) is None) and hasattr(definition, 'default'):
                values[name] = definition.default

            if getattr(definition, 'required', False) and (values.get(name) is None):
                context.validation.report('required %s "%s" must have a value in %s' % (type_name, name, presentation._fullname), locator=presentation._get_child_locator(assignments_field_name), level=Issue.BETWEEN_TYPES)
    
    return values
