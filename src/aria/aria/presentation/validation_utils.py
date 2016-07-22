
from .. import Issue

def validate_no_short_form(presentation, context):
    """
    Makes sure that we can use short form definitions only if we allowed it.
    """
    if (not hasattr(presentation, 'SHORT_FORM_FIELD')) and (not isinstance(presentation._raw, dict)):
        context.validation.report('short form not allowed for field "%s"' % presentation._fullname, locator=presentation._locator, level=Issue.BETWEEN_FIELDS)

def validate_no_unknown_fields(presentation, context):
    """
    Make sure that we can use unknown fields only if we allowed it.
    """
    if (not getattr(presentation, 'ALLOW_UNKNOWN_FIELDS', False)) and (not context.validation.allow_unknown_fields) and isinstance(presentation._raw, dict) and hasattr(presentation, 'FIELDS'):
        for k in presentation._raw:
            if k not in presentation.FIELDS:
                context.validation.report('field "%s" is not supported in "%s"' % (k, presentation._fullname), locator=presentation._get_child_locator(k), level=Issue.BETWEEN_FIELDS)

def validate_known_fields(presentation, context):
    """
    Validates all known fields.
    """
    if hasattr(presentation, '_iter_fields'):
        for _, field in presentation._iter_fields():
            field.validate(presentation, context)

def report_issue_for_unknown_type(context, presentation, type_name, field_name):
    context.validation.report('field "%s" refers to an unknown %s for "%s"' % (getattr(presentation, type_name, field_name), presentation._fullname), locator=presentation._get_child_locator(field_name), level=Issue.BETWEEN_TYPES)

def report_issue_for_parent_is_self(context, presentation, field_name):
    context.validation.report('parent type of "%s" is self' % presentation._fullname, locator=presentation._get_child_locator(field_name), level=Issue.BETWEEN_TYPES)

def report_issue_for_unknown_parent_type(context, presentation, field_name):
    context.validation.report('unknown parent type "%s" for "%s"' % (getattr(presentation, field_name), presentation._fullname), locator=presentation._get_child_locator(field_name), level=Issue.BETWEEN_TYPES)

def report_issue_for_circular_type_hierarchy(context, presentation, field_name):
    context.validation.report('"%s" of "%s" creates a circular type hierarchy' % (getattr(presentation, field_name), presentation._fullname), locator=presentation._get_child_locator(field_name), level=Issue.BETWEEN_TYPES)
