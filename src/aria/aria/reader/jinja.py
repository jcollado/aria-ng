
from .. import VERSION
from ..loader import LiteralLocation, LiteralLoader
from .reader import Reader
from .exceptions import ReaderError
from .yaml import YamlReader
from jinja2 import Template
import os

# TODO: we could put a lot of other useful stuff here.
CONTEXT = {
    'ARIA_VERSION': VERSION,
    'ENV': os.environ}

class JinjaReader(Reader):
    """
    ARIA Jinja reader.
    
    Forwards the rendered result to the reader source's literal reader.
    """

    def read(self):
        data = self.load()
        try:
            data = str(data)
            template = Template(data)
            literal = template.render(CONTEXT)
            # TODO: might be useful to write the literal result to a file for debugging
            next_reader = self.source.get_reader(LiteralLocation(literal), LiteralLoader(literal))
            return next_reader.read()
        except Exception as e:
            raise ReaderError('Jinja: %s' % e, e)
