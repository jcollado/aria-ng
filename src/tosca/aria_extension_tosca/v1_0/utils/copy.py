
#
# NoteTemplate, RelationshipTemplate
#

def get_default_raw_from_copy(presentation, field_name):
    """
    Used for the :code:`_get_default_raw` field hook.
    """
    
    copy = presentation._raw.get('copy')
    if copy is not None:
        templates = getattr(presentation._container, field_name)
        if templates is not None:
            template = templates.get(copy)
            if template is not None:
                return template._raw
    return None
