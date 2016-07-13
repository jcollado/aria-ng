
from .. import Issue, classname
from copy import deepcopy
from collections import OrderedDict

class Presentation(object):
    """
    Base class for ARIA presentations. A presentation is a Pythonic wrapper around
    agnostic raw data, adding the ability to read and modify the data with proper
    validation. 
    
    ARIA presentation classes will often be decorated with @has_fields, as that
    mechanism automates a lot of field-specific validation. However, that is not a
    requirement.
    
    Make sure that your utility property and method names begin with a "_", because
    those names without a "_" prefix are normally reserved for fields. 
    """
    
    def __init__(self, name=None, raw=None):
        self._name = name
        self._raw = raw
        
    def _validate(self, consumption_context):
        self._validate_no_short_form(consumption_context)
        self._validate_no_unknown_fields(consumption_context)
        self._validate_known_fields(consumption_context)
    
    def _validate_no_short_form(self, consumption_context):
        """
        Makes sure that we can use short form definitions only if we allowed it.
        """
        if (not hasattr(self, 'SHORT_FORM_FIELD')) and (not isinstance(self._raw, dict)):
            consumption_context.validation.issues.append(Issue('short form not allowed for %s' % self._fullname, locator=self._locator, level=3))
    
    def _validate_no_unknown_fields(self, consumption_context):
        """
        Make sure that we can use unknown fields only if we allowed it.
        """
        if (not getattr(self, 'ALLOW_UNKNOWN_FIELDS', False)) and (not consumption_context.validation.allow_unknown_fields) and isinstance(self._raw, dict) and hasattr(self, 'FIELDS'):
            for k in self._raw:
                if k not in self.FIELDS:
                    consumption_context.validation.issues.append(Issue('unknown field "%s" in %s' % (k, self._fullname), locator=self._get_child_locator(k), level=3))

    def _validate_known_fields(self, consumption_context):
        """
        Validates all known fields.
        """
        if hasattr(self, '_iter_fields'):
            for _, field in self._iter_fields():
                field.validate(self, consumption_context)

    def _inherit_and_get_dict_field(self, consumption_context, field_name):
        """
        Assumes that we have a \_get\_parent(consumption\_context) method.
        """
        parent = self._get_parent(consumption_context)
        values = parent._inherit_and_get_dict_field(consumption_context, field_name) if parent is not None else OrderedDict()
            
        self_values = getattr(self, field_name)
        if self_values is not None:
            for name, value in self_values.iteritems():
                if name in values:
                    type1 = getattr(values[name], 'type', None)
                    type2 = getattr(value, 'type', None)
                    if type1 != type2:
                        consumption_context.validation.issues.append(Issue('property override changes type from "%s" to "%s" for "%s" in %s' % (type1, type2, name, self._fullname), locator=self._get_grandchild_locator(field_name, name), level=4))
                values[name] = value
            
        return values

    def _get_assigned_and_defined_dict(self, consumption_context, type_name, assignments_field_name, definitions_fn_name):
        """
        Assumes that we have a \_get\_type(consumption\_context) method.
        """
        values = OrderedDict()
        
        the_type = self._get_type(consumption_context)
        assignments = getattr(self, assignments_field_name)
        definitions = getattr(the_type, definitions_fn_name)(consumption_context) if the_type is not None else None

        if assignments is not None:
            for name, assignment in assignments.iteritems():
                if (definitions is None) or (name not in definitions):
                    consumption_context.validation.issues.append(Issue('assignment to undefined %s "%s" in %s' % (type_name, name, self._fullname), locator=self._get_grandchild_locator('properties', name), level=4))
                values[name] = assignment.value
        
        if definitions is not None:
            for name, definition in definitions.iteritems():
                if (values.get(name) is None) and hasattr(definition, 'default'):
                    values[name] = getattr(definition, 'default')
                if getattr(definition, 'required', False) and (values.get(name) is None):
                    consumption_context.validation.issues.append(Issue('required %s "%s" must have a value in %s' % (type_name, name, self._fullname), locator=self._get_child_locator('properties'), level=4))
        
        return values

    def _append_value_error_for_unknown_type(self, consumption_context, type_type, field_name):
        consumption_context.validation.issues.append(Issue('unknown %s type "%s" for %s' % (type_type, getattr(self, field_name), self._fullname), locator=self._get_child_locator(field_name), level=4))

    def _append_issue_for_parent_is_self(self, consumption_context, field_name):
        consumption_context.validation.issues.append(Issue('parent type is self for %s' % self._fullname, locator=self._get_child_locator(field_name), level=4))

    def _append_issue_for_unknown_parent_type(self, consumption_context, field_name):
        consumption_context.validation.issues.append(Issue('unknown parent type "%s" for %s' % (getattr(self, field_name), self._fullname), locator=self._get_child_locator(field_name), level=4))

    def _append_issue_for_circular_type_hierarchy(self, consumption_context, field_name):
        consumption_context.validation.issues.append(Issue('parent type "%s" causes circular type hierarchy for %s' % (getattr(self, field_name), self._fullname), locator=self._get_child_locator(field_name), level=4))

    @property
    def _fullname(self):
        if self._name:
            return '"%s"' % self._name
        return classname(self)

    @property
    def _locator(self):
        if hasattr(self._raw, '_locator'):
            return self._raw._locator
        return None

    def _get_child_locator(self, name):
        locator = self._locator
        return locator.get_child(name) if locator is not None else None

    def _get_grandchild_locator(self, name1, name2):
        locator = self._locator
        return locator.get_grandchild(name1, name2) if locator is not None else None

    def _clone(self):
        raw = deepcopy(self._raw)
        return self.__class__(name=self._name, raw=raw)

class AsIsPresentation(object):
    """
    Base class for trivial ARIA presentations that provide the raw value as is.
    """
    
    def __init__(self, name=None, raw=None):
        self._name = name
        self._raw = raw
    
    @property
    def value(self):
        return self._raw
    
    @value.setter
    def value(self, value):
        self._raw = value

    def _validate(self, consumption_context):
        pass
