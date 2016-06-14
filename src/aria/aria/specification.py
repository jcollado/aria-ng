
TOSCA_SPECIFICATION = {}

def tosca_specification(section, spec='tosca-simple-profile-1.0'):
    """
    Decorator for TOSCA specification.
    
    Used for documentation and standards compliance.
    """
    
    def decorator(o):
        sp = TOSCA_SPECIFICATION.get(spec)
        if sp is None:
            sp = {}
            TOSCA_SPECIFICATION[spec] = sp
        if section in sp:
            raise Exception('You cannot specify the same @tosca_specification twice, consider adding \'-1\', \'-2\', etc.: %s' % section)
        sp[section] = {'code': '%s.%s' % (o.__module__, o.__name__)}
        try:
            setattr(o, TOSCA_SPECIFICATION, {section: section, spec: spec})
        except:
            pass
        return o
    return decorator
