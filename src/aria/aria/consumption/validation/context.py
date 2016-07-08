
from clint.textui import puts, colored, indent

class ValidationContext(object):
    def __init__(self):
        self.issues = []
        self.allow_unknown_fields = False

    def dump_issues(self):
        if self.issues:
            puts(colored.red('Validation issues:'))
            with indent(2):
                for issue in self.issues:
                    puts('%s' % issue)
            return True
        return False
