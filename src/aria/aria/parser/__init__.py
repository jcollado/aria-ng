
from aria import AriaError, UnimplementedAriaError, classname
from aria.loader import DefaultLoaderSource
from aria.reader import DefaultReaderSource
from aria.grammar import DefaultGrammarSource, GrammarNotFoundGrammarError

class ParserError(AriaError):
    """
    ARIA parser error.
    """

class Parser(object):
    """
    Base class for ARIA parsers.
    
    Parsers generate agnostic data structures by consuming a data source via appropriate
    :class:`aria.loader.Loader`, :class:`aria.reader.Reader`, and :class:`aria.grammar.Grammar`
    instances.
    
    Note that parsing may internally trigger more than one loading/reading cycle,
    for example if the agnostic data structure has dependencies that must also be
    parsed.
    """
    
    def __init__(self, locator, loader_source=DefaultLoaderSource(), reader_source=DefaultReaderSource(), grammar_source=DefaultGrammarSource()):
        self.locator = locator
        self.loader_source = loader_source
        self.reader_source = reader_source
        self.grammar_source = grammar_source

    def consume(self, locator):
        raise UnimplementedAriaError(classname(self) + '.parse')

class DefaultParser(Parser):
    """
    The default ARIA parser supports agnostic data structure composing for grammars
    that have get_import_locators.
    """
    
    def consume(self):
        return self._parse_composite(self.locator, None, None)

    def _parse_composite(self, locator, origin_locator, grammar_cls):
        structure = self._parse_one(locator, origin_locator)
        
        if not grammar_cls:
            try:
                grammar_cls = self.grammar_source.get_grammar(structure)
            except GrammarNotFoundGrammarError:
                pass
        
        # Handle imports
        if grammar_cls:
            grammar = grammar_cls(structure)
            if hasattr(grammar, 'get_import_locators'):
                imports = grammar.get_import_locators()
                for import_locator in imports:
                    imported_structure = self._parse_composite(import_locator, locator, grammar_cls)
                    # TODO: too primitive! what if there are conflicts?
                    # also, recursion is not the best idea :/
                    structure.update(imported_structure)

        return structure
    
    def _parse_one(self, locator, origin_locator):
        loader = self.loader_source.get_loader(locator, origin_locator)
        reader = self.reader_source.get_reader(locator, loader)
        return reader.consume()
