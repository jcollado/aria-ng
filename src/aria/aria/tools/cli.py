#!/usr/bin/env python

from aria import *
from aria.reader import *
from aria.parser import *
from aria.consumer import *
from aria.presenter import *
from tosca.datatypes import *

from clint.arguments import Args 
from clint.textui import puts, colored, indent

if __name__ == '__main__':

    args = Args()

    #reader = YamlReader('simple-blueprint.yaml')
    #reader.read()

    r = Credential({'properties': {'protocol': 'http'}})
    print r.properties.protocol

    parser = DefaultParser('blueprints/simple-blueprint.yaml')
    presentation = parser.parse()

    #Writer(structure).consume()

    validator = Validator(presentation)
    validator.consume()

    profile = presentation.profile

    print profile.tosca_definitions_version
    for name, n in profile.node_templates.iteritems():
        print name + ' ' + n.type
