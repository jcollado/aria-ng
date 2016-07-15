
from .. import Issue
from .validation_utils import report_issue_for_unknown_type, report_issue_for_parent_is_self, report_issue_for_unknown_parent_type, report_issue_for_circular_type_hierarchy

def value_validator(type_field_name, get_type_fn):
    """
    Can be used with @field\_validator.
    """
    
    def fn(field, presentation, context):
        field._validate(presentation, context)
        
        # Make sure value can be coerced to the type
        value = getattr(presentation, field.name)
        if value is not None:
            the_type = getattr(presentation, type_field_name)
            if the_type is not None:
                cls = get_type_fn(the_type)
                if cls is not None:
                    try:
                        cls(value)
                    except ValueError:
                        context.validation.report('"%s" must be coercible to %s.%s in %s: %s' % (field.name, cls.__module__, cls.__name__, presentation._fullname, repr(value)), locator=presentation._get_child_locator(field.name), level=Issue.BETWEEN_FIELDS)
        
    return fn

def type_validator(type_name, types_dict_name):
    """
    Can be used with @field\_validator.
    """
    
    def fn(field, presentation, context):
        field._validate(presentation, context)
        
        # Make sure type exists
        value = getattr(presentation, field.name)
        if value is not None:
            types_dict = getattr(context.presentation, types_dict_name) or {}
            if value not in types_dict:
                report_issue_for_unknown_type(context, presentation, type_name, field.name)
        
    return fn

def list_type_validator(type_name, types_dict_name):
    """
    Can be used with @field\_validator.
    """

    def fn(field, presentation, context):
        field._validate(presentation, context)
        
        # Make sure type exists
        values = getattr(presentation, field.name)
        if values is not None:
            types_dict = getattr(context.presentation, types_dict_name) or {}
            for value in values:
                if value not in types_dict:
                    report_issue_for_unknown_type(context, presentation, type_name, field.name)
        
    return fn

def derived_from_validator(types_dict_name):
    """
    Can be used with @field\_validator.
    """

    def fn(field, presentation, context):
        field._validate(presentation, context)
    
        value = getattr(presentation, field.name)
        if value is not None:
            types_dict = getattr(context.presentation, types_dict_name) or {}
            
            # Make sure not derived from self
            if value == presentation._name:
                report_issue_for_parent_is_self(context, presentation, field.name)
            # Make sure derived from type exists
            elif value not in types_dict:
                report_issue_for_unknown_parent_type(context, presentation, field.name)
            else:
                # Make sure derivation hierarchy is not circular
                hierarchy = [presentation._name]
                p = presentation
                while p.derived_from is not None:
                    if p.derived_from == p._name:
                        # This should cause a validation issue at that type
                        break
                    elif p.derived_from not in types_dict:
                        # This should cause a validation issue at that type
                        break
                    p = types_dict[p.derived_from]
                    if p._name in hierarchy:
                        report_issue_for_circular_type_hierarchy(context, presentation, field.name)
                        break
                    hierarchy.append(p._name)

    return fn
