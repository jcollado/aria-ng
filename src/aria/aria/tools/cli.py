
from aria import *
from aria.reader import *
from aria.parser import *
from aria.generator import *
from aria.grammar import *
from tosca.datatypes import *

from clint.arguments import Args 
from clint.textui import puts, colored, indent

args = Args()

#reader = YamlReader('simple-blueprint.yaml')
#reader.read()

r = Credential({'properties': {'protocol': 'http'}})
print r.properties.protocol

parser = DefaultParser('blueprints/simple-blueprint.yaml')
structure = parser.consume()

#Writer(structure).consume()

validator = Validator(structure)
validator.consume()

grammar_cls = parser.grammar_source.get_grammar(structure)
profile = grammar_cls(structure).profile

print profile.tosca_definitions_version
for name, n in profile.node_templates.iteritems():
    print name + ' ' + n.type
