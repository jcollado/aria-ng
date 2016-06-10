
from aria import AriaError, UnimplementedAriaError, classname
from aria.grammar import DefaultGrammarSource
import ruamel.yaml as yaml
import sys

class GeneratorError(AriaError):
    """
    ARIA generator error.
    """
    pass

class Generator(object):
    """
    Base class for ARIA generators.
    
    Generators provide useful functionality by consuming agnostic data structures.
    """
    
    def __init__(self, structure):
        self.structure = structure
    
    def consume(self):
        raise UnimplementedAriaError(classname(self) + '.consume')

class Writer(Generator):
    """
    ARIA writer.
    
    Outputs the agnostic data structure as prettified YAML text.
    """
    
    def __init__(self, structure, out=sys.stdout):
        super(Writer, self).__init__(structure)
        self.out = out
        
    def consume(self):
        try:
            text = yaml.dump(self.structure, Dumper=yaml.RoundTripDumper)
            self.out.write(text)
        except e:
            raise GeneratorError('Writer', e)
        

class Validator(Generator):
    """
    ARIA validator.
    
    Validates the agnostic data structure according to its grammar.
    """
    
    def __init__(self, structure, grammar_source=DefaultGrammarSource()):
        super(Validator, self).__init__(structure)
        self.grammar_source = grammar_source

    def consume(self):
        pass
