
from clint.textui import puts, colored, indent

class Style(object):
    def __init__(self, indentation=2):
        self.indentation = 2
    
    @property
    def indent(self):
        return indent(self.indentation)

    def section(self, value):
        return colored.cyan(value, bold=True)
    
    def type(self, value):
        return colored.blue(value, bold=True)

    def node(self, value):
        return colored.red(value, bold=True)
    
    def property(self, value):
        return colored.magenta(value, bold=True)

    def literal(self, value):
        return colored.yellow(repr(value), bold=True)
