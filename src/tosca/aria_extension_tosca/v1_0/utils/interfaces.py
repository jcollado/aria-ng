
from .properties import coerce_property_value
from collections import OrderedDict
from aria import Issue, merge
from copy import deepcopy

#
# InterfaceType
#

def get_inherited_operations(context, presentation):
    # Get operations from parent
    parent = presentation._get_parent(context)
    operations = get_inherited_operations(context, parent) if parent is not None else OrderedDict()
    
    # Add/merge our operations
    our_operations = presentation.operations
    if our_operations is not None:
        merge_operation_definitions(context, operations, our_operations, presentation._name, presentation, 'type')

    return operations

#
# InterfaceDefinitionForType
#

def get_and_override_input_definitions_from_type(context, presentation):
    inputs = OrderedDict()

    # Get inputs from type
    the_type = presentation._get_type(context) # IntefaceType
    type_inputs = the_type._get_inputs(context) if the_type is not None else None
    if type_inputs is not None:
        for input_name, type_input in type_inputs.iteritems():
            inputs[input_name] = type_input._clone(presentation)

    # Add/merge our inputs
    our_inputs = presentation.inputs
    if our_inputs is not None:
        merge_input_definitions(context, inputs, our_inputs, presentation._name, None, presentation, 'definition')
    
    return inputs

def get_and_override_operation_definitions_from_type(context, presentation):
    operations = OrderedDict()

    # Get operations from type
    the_type = presentation._get_type(context) # InterfaceType
    type_operations = the_type._get_operations(context) if the_type is not None else None
    if type_operations is not None:
        for operations_name, type_operation in type_operations.iteritems():
            operations[operations_name] = type_operation._clone(presentation)
    
    # Add/merge our operations
    our_operations = presentation.operations
    if our_operations is not None:
        merge_operation_definitions(context, operations, our_operations, presentation._name, presentation, 'definition')
    
    return operations

#
# NodeType, RelationshipType, GroupType
#

def get_inherited_interface_definitions(context, presentation, type_name, for_presentation=None):
    # Get interfaces from parent
    parent = presentation._get_parent(context)
    interfaces = get_inherited_interface_definitions(context, parent, type_name, presentation) if parent is not None else OrderedDict()

    # Add/merge interfaces from their types
    merge_interface_definitions_from_their_types(context, interfaces,  presentation)

    # Add/merge our interfaces
    our_interfaces = presentation.interfaces
    if our_interfaces is not None:
        merge_interface_definitions(context, interfaces, our_interfaces, presentation, for_presentation=for_presentation)
    
    return interfaces

#
# NodeTemplate, RelationshipTemplate, GroupDefinition
#

def get_template_interfaces(context, presentation, type_name):
    interfaces = OrderedDict()
    
    the_type = presentation._get_type(context) # e.g. NodeType
    type_interfaces = the_type._get_interfaces(context) if the_type is not None else None

    # Fill in interfaces from the type (will initialize with default values)
    if type_interfaces is not None:
        for interface_name, interface in type_interfaces.iteritems():
            interfaces[interface_name] = convert_interface_definition_from_type_to_template(context, interface, presentation)
    
    # Fill in our interfaces
    our_interfaces = presentation.interfaces
    if our_interfaces is not None:
        for interface_name, our_interface in our_interfaces.iteritems():
            if interface_name in interfaces:
                interface = interfaces[interface_name] # InterfaceDefinitionForTemplate
                type_interface = type_interfaces[interface_name] # InterfaceDefinitionForType
                
                # Check if we changed the interface type
                interface_type1 = type_interface.type
                interface_type2 = our_interface.type
                if (interface_type1 is not None) and (interface_type2 is not None) and (interface_type1 != interface_type2):
                    context.validation.report('interface definition "%s" changes interface type from "%s" to "%s" for "%s"' % (interface_name, interface_type1, interface_type2, presentation._fullname), locator=getattr(interface_type2, '_locator', our_interface._locator), level=Issue.BETWEEN_TYPES)

                # Assign interface inputs
                assign_raw_inputs(context, interface._raw, our_interface.inputs, type_interface._get_inputs(context), our_interface, interface_name, None, presentation)
                    
                # Assign operation implementations and inputs
                our_operations = our_interface.operations
                type_operations = type_interface._get_operations(context)
                if our_operations is not None:
                    for operation_name, our_operation in our_operations.iteritems():
                        type_operation = type_operations.get(operation_name) # OperationDefinitionForType

                        our_inputs = our_operation.inputs # OperationDefinitionForTemplate
                        our_implementation = our_operation.implementation
                        
                        if type_operation is None:
                            context.validation.report('interface definition "%s" refers to an unknown operation "%s" for "%s"' % (interface_name, operation_name, presentation._fullname), locator=our_operation._locator, level=Issue.BETWEEN_TYPES)

                        if (our_inputs is not None) or (our_implementation is not None):
                            # Make sure we have the dict
                            if (operation_name not in interface._raw) or (interface._raw[operation_name] is None):
                                interface._raw[operation_name] = {}
                            
                        if our_implementation is not None:
                            interface._raw[operation_name]['implementation'] = deepcopy(our_implementation._raw)

                        # Assign operation inputs
                        type_inputs = type_operation.inputs if type_operation is not None else None
                        assign_raw_inputs(context, interface._raw[operation_name], our_inputs, type_inputs, our_operation, interface_name, operation_name, presentation)

                # Check that there are no required inputs for operations we haven't assigned
                validate_unassigned_operation_inputs(context, interface.operations, type_operations, our_interface, presentation)
            else:
                context.validation.report('interface definition "%s" not declared in %s "%s" for "%s"' % (interface_name, type_name, presentation.type, presentation._fullname), locator=our_interface._locator, level=Issue.BETWEEN_TYPES)

    return interfaces

#
# Utils
#

def convert_input_definitions_to_values(values, definitions):
    for name, definition in definitions.iteritems():
        default = definition.default
        if default is not None:
            values[name] = default

def convert_interface_definition_from_type_to_template(context, presentation, container):
    raw = {}
    
    raw['type'] = presentation.type
    
    # Copy default values for inputs
    inputs = presentation._get_inputs(context)
    if inputs is not None:
        raw['inputs'] = {}
        convert_input_definitions_to_values(raw['inputs'], inputs)
    
    # Copy operations
    operations = presentation._get_operations(context)
    if operations is not None:
        raw['operations'] = {}
        for operation_name, operation in operations.iteritems():
            raw['operations'][operation_name] = {}
            description = operation.description
            if description is not None:
                raw['operations'][operation_name]['description'] = deepcopy(description)
            implementation = operation.implementation
            if implementation is not None:
                raw['operations'][operation_name]['implementation'] = deepcopy(implementation._raw)
            inputs = operation.inputs
            if inputs is not None:
                raw['operations'][operation_name]['inputs'] = {}
                convert_input_definitions_to_values(raw['operations'][operation_name]['inputs'], inputs)
    
    from ..definitions import InterfaceDefinitionForTemplate
    return InterfaceDefinitionForTemplate(name=presentation._name, raw=raw, container=container)

def merge_raw_input_definition(context, raw_input, our_input, interface_name, operation_name, presentation, type_name):
    # Check if we changed the type
    input_type1 = raw_input.get('type')
    input_type2 = our_input.type
    if input_type1 != input_type2:
        if operation_name is not None:
            context.validation.report('interface %s "%s" changes operation input "%s.%s" type from "%s" to "%s" for "%s"' % (type_name, interface_name, operation_name, our_input._name, input_type1, input_type2, presentation._fullname), locator=input_type2._locator, level=Issue.BETWEEN_TYPES)
        else:
            context.validation.report('interface %s "%s" changes input "%s" type from "%s" to "%s" for "%s"' % (type_name, interface_name, our_input._name, input_type1, input_type2, presentation._fullname), locator=input_type2._locator, level=Issue.BETWEEN_TYPES)

    # Merge    
    merge(raw_input, our_input._raw)

def merge_input_definitions(context, inputs, our_inputs, interface_name, operation_name, presentation, type_name):
    for input_name, our_input in our_inputs.iteritems():
        if input_name in inputs:
            merge_raw_input_definition(context, inputs[input_name]._raw, our_input, interface_name, operation_name, presentation, type_name)
        else:
            inputs[input_name] = our_input._clone(presentation)

def merge_raw_input_definitions(context, raw_inputs, our_inputs, interface_name, operation_name, presentation, type_name):
    for input_name, our_input in our_inputs.iteritems():
        if input_name in raw_inputs:
            merge_raw_input_definition(context, raw_inputs[input_name], our_input, interface_name, operation_name, presentation, type_name)
        else:
            raw_inputs[input_name] = deepcopy(our_input._raw)

def merge_raw_operation_definition(context, raw_operation, our_operation, interface_name, presentation, type_name):
    # Add/merge inputs
    our_operation_inputs = our_operation.inputs
    if our_operation_inputs is not None:
        # Make sure we have the dict
        if ('inputs' not in raw_operation) or (raw_operation.get('inputs') is None):
            raw_operation['inputs'] = {}
            
        merge_raw_input_definitions(context, raw_operation['inputs'], our_operation_inputs, interface_name, our_operation._name, presentation, type_name)
    
    # Override the description
    if our_operation._raw.get('description') is not None:
        raw_operation['description'] = deepcopy(our_operation._raw['description'])
    
    # Add/merge implementation
    if our_operation._raw.get('implementation') is not None:
        if raw_operation.get('implementation') is not None:
            merge(raw_operation['implementation'], deepcopy(our_operation._raw['implementation']))
        else:
            raw_operation['implementation'] = deepcopy(our_operation._raw['implementation'])

def merge_operation_definitions(context, operations, our_operations, interface_name, presentation, type_name):
    for operation_name, our_operation in our_operations.iteritems():
        if operation_name in operations:
            merge_raw_operation_definition(context, operations[operation_name]._raw, our_operation, interface_name, presentation, type_name)
        else:
            operations[operation_name] = our_operation._clone(presentation)

def merge_raw_operation_definitions(context, raw_operations, our_operations, interface_name, presentation, type_name):
    for operation_name, our_operation in our_operations.iteritems():
        if operation_name in raw_operations:
            merge_raw_operation_definition(context, raw_operations[operation_name], our_operation, interface_name, presentation, type_name)
        else:
            raw_operations[operation_name] = deepcopy(our_operation._raw)

def merge_interface_definition(context, interface, our_source, presentation, type_name): # from either an InterfaceType or an InterfaceDefinition
    if hasattr(our_source, 'type'):
        # Check if we changed the interface type
        input_type1 = interface.type
        input_type2 = our_source.type
        if (input_type1 is not None) and (input_type2 is not None) and (input_type1 != input_type2):
            context.validation.report('interface definition "%s" changes type from "%s" to "%s" for "%s"' % (interface._name, input_type1, input_type2, presentation._fullname), locator=input_type2._locator, level=Issue.BETWEEN_TYPES)
    
    # Add/merge inputs
    our_interface_inputs = our_source._get_inputs(context) if hasattr(our_source, '_get_inputs') else our_source.inputs 
    if our_interface_inputs is not None:
        # Make sure we have the dict
        if ('inputs' not in interface._raw) or (interface._raw.get('inputs') is None):
            interface._raw['inputs'] = {}
    
        merge_raw_input_definitions(context, interface._raw['inputs'], our_interface_inputs, our_source._name, None, presentation, type_name)
        
    # Add/merge operations
    our_operations = our_source._get_operations(context) if hasattr(our_source, '_get_operations') else our_source.operations
    if our_operations is not None:
        merge_raw_operation_definitions(context, interface._raw, our_operations, our_source._name, presentation, type_name)

def merge_interface_definitions(context, interfaces, our_interfaces, presentation, for_presentation=None):
    for name, our_interface in our_interfaces.iteritems():
        if name in interfaces:
            merge_interface_definition(context, interfaces[name], our_interface, presentation, 'definition')
        else:
            if for_presentation is not None:
                interfaces[name] = our_interface._clone(for_presentation)
            else:
                interfaces[name] = our_interface

def merge_interface_definitions_from_their_types(context, interfaces, presentation):
    for interface in interfaces.itervalues():
        the_type = interface._get_type(context) # InterfaceType
        if the_type is not None:
            merge_interface_definition(context, interface, the_type, presentation, 'type')

def assign_raw_inputs(context, values, assignments, definitions, target, interface_name, operation_name, presentation):
    if assignments is not None:
        # Make sure we have the dict
        if ('inputs' not in values) or (values['inputs'] is None):
            values['inputs'] = {}

        # Assign inputs
        for input_name, assignment in assignments.iteritems():
            if (definitions is not None) and (input_name not in definitions):
                if operation_name is not None:
                    context.validation.report('interface definition "%s" assigns a value to an unknown operation input "%s.%s" for "%s"' % (interface_name, operation_name, input_name, presentation._fullname), locator=assignment._locator, level=Issue.BETWEEN_TYPES)
                else:
                    context.validation.report('interface definition "%s" assigns a value to an unknown input "%s" for "%s"' % (interface_name, input_name, presentation._fullname), locator=assignment._locator, level=Issue.BETWEEN_TYPES)

            definition = definitions.get(input_name) if definitions is not None else None
            
            # Coerce value
            value = coerce_property_value(context, assignment, definition)
            values['inputs'][input_name] = value

    # Check that required inputs are assigned
    if definitions is not None:
        for input_name, definition in definitions.iteritems():
            if definition.required and (values['inputs'] is not None) and (values['inputs'].get(input_name) is None):
                if operation_name is not None:
                    context.validation.report('interface definition "%s" does not assign a value to a required operation input "%s.%s" for "%s"' % (interface_name, operation_name, input_name, presentation._fullname), locator=target._locator, level=Issue.BETWEEN_TYPES)
                else:
                    context.validation.report('interface definition "%s" does not assign a value to a required input "%s" for "%s"' % (interface_name, input_name, presentation._fullname), locator=target._locator, level=Issue.BETWEEN_TYPES)

def validate_unassigned_operation_inputs(context, operations, definitions, interface, presentation):
    for operation_name, definition in definitions.iteritems():
        definition_inputs = definition.inputs if definition is not None else None
        if definition_inputs is not None:
            for input_name, definition_input in definition_inputs.iteritems():
                if definition_input.required:
                    if operation_name not in operations: 
                        context.validation.report('interface definition "%s" does not assign a value to a required operation input "%s.%s" for "%s"' % (interface._name, operation_name, input_name, presentation._fullname), locator=interface._locator, level=Issue.BETWEEN_TYPES)
