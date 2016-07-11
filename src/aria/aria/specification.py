
from collections import OrderedDict

DSL_SPECIFICATION = {}
DSL_SPECIFICATION_PACKAGES = []

URL = {
    'tosca-simple-profile-1.0': 'http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html',
    'tosca-simple-nfv-1.0': 'http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/tosca-nfv-v1.0.html'}

def dsl_specification(section, spec):
    """
    Decorator for TOSCA specification.
    
    Used for documentation and standards compliance.
    """
    
    def decorator(o):
        sp = DSL_SPECIFICATION.get(spec)
        if sp is None:
            sp = {}
            DSL_SPECIFICATION[spec] = sp
        if section in sp:
            raise Exception('you cannot specify the same @dsl_specification twice, consider adding \'-1\', \'-2\', etc.: %s, %s' % (spec, section))

        url = URL.get(spec)
        if url:
            doc = o.__doc__
            if doc is not None:
                url_start = doc.find(url)
                if url_start != -1:
                    url_end = doc.find('>', url_start + len(url))
                    if url_end != -1:
                        url = doc[url_start:url_end]

        sp[section] = OrderedDict((
            ('code', '%s.%s' % (o.__module__, o.__name__)),
            ('url', url)))
        try:
            setattr(o, DSL_SPECIFICATION, {section: section, spec: spec})
        except:
            pass
        return o
    return decorator

def iter_spec(spec):
    sections = DSL_SPECIFICATION[spec]
    keys = sections.keys()
    def key(value):
        try:
            k = 0.0
            level = 1.0
            parts = value.split('-', 1)
            for part in parts[0].split('.'):
                k += float(part) / level
                level *= 1000.0
            if len(parts) > 1:
                k += float(parts[1]) / level
            return k
        except ValueError:
            return value
    keys.sort(key=key)
    for key in keys:
        yield key, sections[key]
