
from aria import AriaError, UnimplementedAriaError, classname

class GrammarError(AriaError):
    """
    ARIA grammar error.
    """
    pass

class GrammarNotFoundGrammarError(GrammarError):
    """
    ARIA grammar error: grammar not found for structure.
    """
    pass

class Grammar(object):
    """
    Base class for ARIA grammars.
    
    Grammars provide a robust API over agnostic data structures.
    """
    
    def __init__(self, structure={}):
        self.structure = structure

class GrammarSource(object):
    """
    Base class for ARIA grammar sources.
    
    Grammar sources provide appropriate :class:`Grammar` classes for agnostic data structures.
    """

    def get_grammar(self, structure):
        raise UnimplementedAriaError(classname(self) + '.get_grammar')

class DefaultGrammarSource(GrammarSource):
    """
    The default ARIA grammar source supports TOSCA Simple Profile v1.0 and Cloudify.
    """

    def get_grammar(self, structure):
        tosca_definitions_version = structure.get('tosca_definitions_version')
        if tosca_definitions_version == 'tosca_simple_yaml_1_0':
            import aria.grammar.tosca_simple
            return aria.grammar.tosca_simple.ToscaSimpleGrammar1_0
        elif tosca_definitions_version == 'cloudify_dsl_1_3':
            import aria.grammar.cloudify
            return aria.grammar.cloudify.CloudifyGrammar1_3
        else:
            raise GrammarNotFoundGrammarError(tosca_definitions_version)
