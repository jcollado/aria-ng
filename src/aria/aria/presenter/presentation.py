
class Presentation(object):
    def __init__(self, raw={}):
        self.raw = raw
        
    def validate(self, issues):
        if hasattr(self, 'iter_fields'):
            for _, field in self.iter_fields():
                field.validate(self, issues)
