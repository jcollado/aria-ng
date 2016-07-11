
from .. import Issue, classname
from copy import deepcopy

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
        self._allow_unknown_fields = False
        
    def _validate(self, consumption_context):
        # Check for short form
        if not hasattr(self.__class__, 'SHORT_FORM_FIELD') and not isinstance(self._raw, dict):
            consumption_context.validation.issues.append(Issue('short form not allowed for %s' % self._fullname, map=self._map))
        
        # Check for unknown fields
        if (not self._allow_unknown_fields) and (not consumption_context.validation.allow_unknown_fields) and isinstance(self._raw, dict) and hasattr(self, 'FIELDS'):
            for k in self._raw:
                if k not in self.FIELDS:
                    consumption_context.validation.issues.append(Issue('unknown field "%s" in %s' % (k, self._fullname), map=self._get_child_map(k)))

        # Validate fields
        if hasattr(self, '_iter_fields'):
            for _, field in self._iter_fields():
                field.validate(self, consumption_context)
    
    def _append_issue_for_unknown_type(self, consumption_context, type_type, field_name):
        consumption_context.validation.issues.append(Issue('unknown %s type "%s" for %s' % (type_type, getattr(self, field_name), self._fullname), map=self._get_child_map(field_name)))

    def _append_issue_for_parent_is_self(self, consumption_context, field_name):
        consumption_context.validation.issues.append(Issue('parent type is self for %s' % self._fullname, map=self._get_child_map(field_name)))

    def _append_issue_for_unknown_parent_type(self, consumption_context, field_name):
        consumption_context.validation.issues.append(Issue('unknown parent type "%s" for %s' % (getattr(self, field_name), self._fullname), map=self._get_child_map(field_name)))

    def _append_issue_for_circular_type_hierarchy(self, consumption_context, field_name):
        consumption_context.validation.issues.append(Issue('parent type "%s" causes circular type hierarchy for %s' % (getattr(self, field_name), self._fullname), map=self._get_child_map(field_name)))

    @property
    def _fullname(self):
        if self._name:
            return '"%s"' % self._name
        return classname(self)

    @property
    def _map(self):
        if hasattr(self._raw, '_map'):
            return self._raw._map
        return None

    def _get_child_map(self, name):
        if hasattr(self._raw, '_map'):
            return self._raw._map.children.get(name) or self._raw._map
        return None

    def _clone(self):
        raw = deepcopy(self._raw)
        return self.__class__(name=self._name, raw=raw)
