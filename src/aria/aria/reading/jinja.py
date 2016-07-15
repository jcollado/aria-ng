
from .. import VERSION
from ..loading import LiteralLocation, LiteralLoader
from .reader import Reader
from .exceptions import SyntaxError
from jinja2 import Template
import os

# TODO: we could put a lot of other useful stuff here.
CONTEXT = {
    'ARIA_VERSION': VERSION,
    'ENV': os.environ}

class JinjaReader(Reader):
    """
    ARIA Jinja reader.
    
    Forwards the rendered result to a new reader in the reader source.
    """

    def read(self):
        data = self.load()
        try:
            data = str(data)
            template = Template(data)
            literal = template.render(CONTEXT)
            # TODO: might be useful to write the literal result to a file for debugging
            location = self.location
            if isinstance(location, basestring) and location.endswith('.jinja'):
                # Use reader based on the location with the ".jinja" prefix stripped off
                location =  '<literal> ' + location[:-6]
                next_reader = self.source.get_reader(location, LiteralLoader(literal, location=location))
            else:
                # Use reader for literal loader
                next_reader = self.source.get_reader(LiteralLocation(literal), LiteralLoader(literal))
            return next_reader.read()
        except Exception as e:
            raise SyntaxError('Jinja: %s' % e, cause=e)
