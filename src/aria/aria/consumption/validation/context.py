
from ... import Issue, ReadOnlyList, print_exception
from clint.textui import puts, colored, indent

class ValidationContext(object):
    def __init__(self):
        self._issues = []
        self.allow_unknown_fields = False
        self.max_level = Issue.ALL

    def report(self, message=None, exception=None, location=None, line=None, column=None, locator=None, snippet=None, level=Issue.PLATFORM, issue=None):
        if issue is None:
            issue = Issue(message, exception, location, line, column, locator, snippet, level)

        # Avoid duplicate issues        
        for i in self._issues:
            if str(i) == str(issue):
                return
            
        self._issues.append(issue)

    @property
    def issues(self):
        issues = [i for i in self._issues if i.level <= self.max_level] 
        issues.sort(key=lambda i: i.level)
        return ReadOnlyList(issues)

    def dump_issues(self):
        issues = self.issues
        if issues:
            puts(colored.blue('Validation issues:', bold=True))
            with indent(2):
                for issue in issues:
                    puts(colored.blue(issue.heading_as_str))
                    details = issue.details_as_str
                    if details:
                        with indent(3):
                            puts(details)
                    if issue.exception is not None:
                        with indent(3):
                            print_exception(issue.exception)
            return True
        return False
