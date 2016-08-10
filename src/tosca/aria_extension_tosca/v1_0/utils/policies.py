
#
# PolicyType
#

def get_inherited_targets(context, presentation):
    """
    Returns our target node types and group types if we have them or those of our parent, if we have one (recursively).
    """
    
    parent = presentation._get_parent(context)
    
    node_types, group_types = get_inherited_targets(context, parent) if parent is not None else ([], [])
    
    our_targets = presentation.targets
    if our_targets:
        all_node_types = context.presentation.node_types or {} 
        all_group_types = context.presentation.group_types or {}
        node_types = []
        group_types = [] 
        
        for our_target in our_targets:
            if our_target in all_node_types:
                node_types.append(all_node_types[our_target])
            elif our_target in all_group_types:
                group_types.append(all_group_types[our_target])
    
    return node_types, group_types

#
# PolicyDefinition
#

def get_policy_targets(context, presentation):
    """
    Returns our target node templates and groups if we have them.
    """
    
    node_templates = []
    groups = []

    our_targets = presentation.targets
    if our_targets:
        all_node_templates = context.presentation.node_templates or {} 
        all_groups = context.presentation.groups or {}
        
        for our_target in our_targets:
            if our_target in all_node_templates:
                node_templates.append(all_node_templates[our_target])
            elif our_target in all_groups:
                groups.append(all_groups[our_target])
    
    return node_templates, groups
