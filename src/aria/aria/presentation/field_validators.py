
from .. import Issue
from .utils import report_issue_for_unknown_type, report_issue_for_parent_is_self, report_issue_for_unknown_parent_type, report_issue_for_circular_type_hierarchy

def type_validator(type_name, types_dict_name):
    """
    Makes sure that the field refers to an existing type defined in the root presenter.
    
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
    Makes sure that the field's elements refer to existing types defined in the root presenter.
    
    Assumes that the field is a list.
    
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

def list_length_validator(length):
    """
    Makes sure the field has exactly a specific number of elements.
    
    Assumes that the field is a list.
    
    Can be used with @field\_validator.
    """

    def fn(field, presentation, context):
        field._validate(presentation, context)
        
        # Make sure list has exactly the length
        values = getattr(presentation, field.name)
        if isinstance(values, list):
            if len(values) != length:
                context.validation.report('field "%s" does not have exactly %d elements for "%s"' % (field.name, length, presentation._fullname), locator=presentation._get_child_locator(field.name), level=Issue.FIELD)
        
    return fn

def derived_from_validator(types_dict_name):
    """
    Makes sure that the field refers to a valid parent type defined in the root presenter.
    
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
