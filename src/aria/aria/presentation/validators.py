
def type_validator(type_type, types_dict_name):
    def fn(field, presentation, consumption_context):
        field._validate(presentation, consumption_context)
        
        # Make sure type exists
        value = getattr(presentation, field.name)
        if value is not None:
            types_dict = getattr(consumption_context.presentation, types_dict_name)
            if value not in types_dict:
                presentation._append_value_error_for_unknown_type(consumption_context, type_type, field.name)
        
    return fn

def derived_from_validator(types_dict_name):
    def fn(field, presentation, consumption_context):
        field._validate(presentation, consumption_context)
    
        value = getattr(presentation, field.name)
        if value is not None:
            types_dict = getattr(consumption_context.presentation, types_dict_name)
            
            # Make sure not derived from self
            if value == presentation._name:
                presentation._append_issue_for_parent_is_self(consumption_context, field.name)
            # Make sure derived from type exists
            elif value not in types_dict:
                presentation._append_issue_for_unknown_parent_type(consumption_context, field.name)
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
                        presentation._append_issue_for_circular_type_hierarchy(consumption_context, field.name)
                        break
                    hierarchy.append(p._name)

    return fn