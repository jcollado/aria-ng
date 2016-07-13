
from ... import print_exception
from clint.textui import puts, colored, indent

class ValidationContext(object):
    def __init__(self):
        self.issues = []
        self.allow_unknown_fields = False

    def dump_issues(self):
        if self.issues:
            puts(colored.red('Validation issues:'))
            with indent(2):
                for issue in sorted(self.issues, key=lambda x: x.level):
                    puts('%s' % issue)
                    if issue.exception is not None:
                        with indent(2):
                            print_exception(issue.exception)
            return True
        return False
