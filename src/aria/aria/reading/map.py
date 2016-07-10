
from clint.textui import puts, colored, indent

class Map(object):
    """
    Stores location information (line and column numbers) for agnostic raw data.
    """
    def __init__(self, location, line, column):
        self.location = location
        self.line = line
        self.column = column
        self.children = None
    
    def link(self, raw):
        if isinstance(raw, list):
            setattr(raw, '_map', self)
            for i in range(len(raw)):
                r = raw[i]
                if isinstance(r, list) or isinstance(r, dict):
                    self.children[i].link(r)
        elif isinstance(raw, dict):
            setattr(raw, '_map', self)
            for k, r in raw.iteritems():
                if isinstance(r, list) or isinstance(r, dict):
                    try:
                        self.children[k].link(r)
                    except KeyError:
                        raise ValueError('map does not match agnostic raw data: %s' % k)
    
    def merge(self, map):
        if isinstance(self.children, dict) and isinstance(map.children, dict):
            for k, m in map.children.iteritems():
                if k in self.children:
                    self.children[k].merge(m)
                else:
                    self.children[k] = m

    def dump(self, key=None):
        if key:
            puts('%s "%s":%d:%d' % (colored.red(key), colored.blue(self.location), self.line, self.column))
        else:
            puts('"%s":%d:%d' % (colored.blue(self.location), self.line, self.column))
        if isinstance(self.children, list):
            with indent(2):
                for m in self.children:
                    m.dump()
        elif isinstance(self.children, dict):
            with indent(2):
                for k, m in self.children.iteritems():
                    m.dump(k)

    def __str__(self):
        # Should be in same format as Issue.location_as_str
        return '"%s":%d:%d' % (self.location, self.line, self.column)
