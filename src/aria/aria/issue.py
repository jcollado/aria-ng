
class Issue(object):
    def __init__(self, message, exception=None, location=None, line=None, column=None, map=None, snippet=None):
        self.message = str(message)
        self.exception = exception
        if map is not None:
            self.location = map.location
            self.line = map.line
            self.column = map.column
        else:
            self.location = location
            self.line = line
            self.column = column
        self.snippet = snippet

    @property
    def location_as_str(self):
        if self.location is not None:
            if self.line is not None:
                if self.column is not None:
                    return '"%s":%d:%d' % (self.location, self.line, self.column)
                else: 
                    return '"%s":%d' % (self.location, self.line)
            else:
                return '"%s"' % self.location
        else:
            return None

    def __str__(self):
        r = self.message
        location = self.location_as_str
        if location is not None:
            r += ', at %s' % location
        if self.snippet is not None:
            r += '\n%s' % self.snippet
        if self.exception is not None:
            r += '\n%s' % self.exception
        return r
