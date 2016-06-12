
class Presentation(object):
    def __init__(self, raw={}):
        self.raw = raw
        
    def validate(self, issues):
        if hasattr(self.__class__, 'FIELDS'):
            for field in self.__class__.FIELDS.itervalues():
                field.validate(self, issues)
