
from collections import OrderedDict

TOSCA_SPECIFICATION = {}

URL = {
    'tosca-simple-profile-1.0': 'http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html',
    'tosca-simple-nfv-1.0': 'http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/tosca-nfv-v1.0.html'}

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

        url = URL.get(spec)
        if url:
            doc = o.__doc__
            url_start = doc.find(url)
            if url_start != -1:
                url_end = doc.find('>', url_start + len(url))
                if url_end != -1:
                    url = doc[url_start:url_end]

        sp[section] = OrderedDict((
            ('code', '%s.%s' % (o.__module__, o.__name__)),
            ('url', url)))
        try:
            setattr(o, TOSCA_SPECIFICATION, {section: section, spec: spec})
        except:
            pass
        return o
    return decorator

def iter_spec(spec):
    sections = TOSCA_SPECIFICATION[spec]
    keys = sections.keys()
    def key(value):
        k = 0.0
        level = 1.0
        parts = value.split('-', 1)
        for part in parts[0].split('.'):
            k += float(part) / level
            level *= 1000.0
        if len(parts) > 1:
            k += float(parts[1]) / level
        return k
    keys.sort(key=key)
    for key in keys:
        yield key, sections[key]
