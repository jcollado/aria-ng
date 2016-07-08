
from .. import Issue, classname
from copy import deepcopy

class Presentation(object):
    def __init__(self, name=None, raw={}):
        self._name = name
        self._raw = raw
        self._allow_unknown_fields = False
        self._allow_short_form = False
        
    def _validate(self, consumption_context):
        if (not self._allow_short_form) and not isinstance(self._raw, dict):
            consumption_context.validation.issues.append(Issue('short form not allowed for %s, %s' % (self._fullname, self._location)))
        
        if (not self._allow_unknown_fields) and (not consumption_context.validation.allow_unknown_fields) and isinstance(self._raw, dict):
            for k in self._raw:
                if k not in self.FIELDS:
                    consumption_context.validation.issues.append(Issue('unknown field "%s" in %s, %s' % (k, self._fullname, self._get_child_location(k))))

        if hasattr(self, '_iter_fields'):
            for _, field in self._iter_fields():
                field.validate(self, consumption_context)
    
    def _append_issue_for_unknown_type(self, consumption_context, type_type, field_name):
        consumption_context.validation.issues.append(Issue('unknown %s type "%s" for %s, %s' % (type_type, getattr(self, field_name), self._fullname, self._get_child_location(field_name))))

    def _append_issue_for_parent_is_self(self, consumption_context, field_name):
        consumption_context.validation.issues.append(Issue('parent type is self for %s, %s' % (self._fullname, self._get_child_location(field_name))))

    def _append_issue_for_unknown_parent_type(self, consumption_context, field_name):
        consumption_context.validation.issues.append(Issue('unknown parent type "%s" for %s, %s' % (getattr(self, field_name), self._fullname, self._get_child_location(field_name))))

    def _append_issue_for_circular_type_hierarchy(self, consumption_context, field_name):
        consumption_context.validation.issues.append(Issue('parent type "%s" causes circular hierarchy for %s, %s' % (getattr(self, field_name), self._fullname, self._get_child_location(field_name))))

    @property
    def _fullname(self):
        if self._name:
            return '"%s"' % self._name
        return classname(self)

    @property
    def _location(self):
        if hasattr(self._raw, '_map'):
            map = self._raw._map
            return 'at %s' % map
        return 'at unknown location'

    def _get_child_location(self, name):
        if hasattr(self._raw, '_map'):
            map = self._raw._map
            map = map.children.get(name, map)
            return 'at %s' % map
        return 'at unknown location'

    def _clone(self):
        raw = deepcopy(self._raw)
        return self.__class__(name=self._name, raw=raw)
