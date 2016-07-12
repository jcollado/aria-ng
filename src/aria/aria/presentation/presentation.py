
from .. import Issue, classname, merge
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
    
    def __init__(self, name=None, raw={}):
        self._name = name
        self._raw = raw
        
    def _validate(self, consumption_context):
        self._validate_short_form(consumption_context)
        self._validate_unknown_fields(consumption_context)
        self._validate_fields(consumption_context)
    
    def _validate_short_form(self, consumption_context):
        if (not hasattr(self, 'SHORT_FORM_FIELD')) and (not isinstance(self._raw, dict)):
            consumption_context.validation.issues.append(Issue('short form not allowed for %s' % self._fullname, locator=self._locator))
    
    def _validate_unknown_fields(self, consumption_context):
        if (not getattr(self, 'ALLOW_UNKNOWN_FIELDS', False)) and (not consumption_context.validation.allow_unknown_fields) and isinstance(self._raw, dict) and hasattr(self, 'FIELDS'):
            for k in self._raw:
                if k not in self.FIELDS:
                    consumption_context.validation.issues.append(Issue('unknown field "%s" in %s' % (k, self._fullname), locator=self._get_child_locator(k)))

    def _validate_fields(self, consumption_context):
        if hasattr(self, '_iter_fields'):
            for _, field in self._iter_fields():
                field.validate(self, consumption_context)

    def _inherit_and_get_dict_field(self, consumption_context, field_name, derived_from_field_name, types_dict_name):
        values = OrderedDict()
        derived_from = getattr(self, derived_from_field_name)
        if derived_from is not None:
            types = getattr(consumption_context.presentation, types_dict_name)
            parent = types.get(derived_from)
            merge(values, parent._inherit_and_get_dict_field(consumption_context, field_name, derived_from_field_name, types_dict_name), strict=False)
        self_values = getattr(self, field_name)
        if self_values is not None:
            merge(values, self_values, strict=False)
        return values

    def _assign_defined_dict(self, consumption_context, type_name, assignments, definitions):
        values = OrderedDict()
        if assignments is not None:
            for name, assignment in assignments.iteritems():
                if (definitions is None) or (name not in definitions):
                    consumption_context.validation.issues.append(Issue('assignment to undefined %s "%s" in %s' % (type_name, name, self._fullname), locator=self._get_grandchild_locator('properties', name)))
                values[name] = assignment.value
        if definitions is not None:
            for name, definition in definitions.iteritems():
                if (values.get(name) is None) and hasattr(definition, 'default'):
                    values[name] = getattr(definition, 'default')
                if getattr(definition, 'required', False) and (values.get(name) is None):
                    consumption_context.validation.issues.append(Issue('required %s "%s" must have a value in %s' % (type_name, name, self._fullname), locator=self._get_child_locator('properties')))
        return values
    
    def _append_issue_for_unknown_type(self, consumption_context, type_type, field_name):
        consumption_context.validation.issues.append(Issue('unknown %s type "%s" for %s' % (type_type, getattr(self, field_name), self._fullname), locator=self._get_child_locator(field_name)))

    def _append_issue_for_parent_is_self(self, consumption_context, field_name):
        consumption_context.validation.issues.append(Issue('parent type is self for %s' % self._fullname, locator=self._get_child_locator(field_name)))

    def _append_issue_for_unknown_parent_type(self, consumption_context, field_name):
        consumption_context.validation.issues.append(Issue('unknown parent type "%s" for %s' % (getattr(self, field_name), self._fullname), locator=self._get_child_locator(field_name)))

    def _append_issue_for_circular_type_hierarchy(self, consumption_context, field_name):
        consumption_context.validation.issues.append(Issue('parent type "%s" causes circular type hierarchy for %s' % (getattr(self, field_name), self._fullname), locator=self._get_child_locator(field_name)))

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
        if hasattr(self._raw, '_locator'):
            return self._raw._locator.children.get(name, self._raw._locator)
        return None

    def _get_grandchild_locator(self, name1, name2):
        if hasattr(self._raw, '_locator'):
            locator = self._raw._locator
            locator2 = self._raw._locator.children.get(name1)
            if locator2 is not None:
                locator3 = locator2.children.get(name2)
                if locator3 is not None:
                    return locator3
                return locator2
            return locator
        return None

    def _clone(self):
        raw = deepcopy(self._raw)
        return self.__class__(name=self._name, raw=raw)
