
from .utils import classname

class Issue(object):
    def __init__(self, message=None, exception=None, location=None, line=None, column=None, locator=None, snippet=None):
        if message is not None:
            self.message = str(message)
        elif exception is not None:
            self.message = 'exception was raised'
        else:
            self.message = 'unknown issue'
            
        self.exception = exception
        
        if locator is not None:
            self.location = locator.location
            self.line = locator.line
            self.column = locator.column
        else:
            self.location = location
            self.line = line
            self.column = column
            
        self.snippet = snippet

    @property
    def locator_as_str(self):
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
        locator = self.locator_as_str
        if locator is not None:
            r += ', at %s' % locator
        if self.snippet is not None:
            r += '\n%s' % self.snippet
        if self.exception is not None:
            r += '\n  %s: %s' % (classname(self.exception), self.exception)
        return r
