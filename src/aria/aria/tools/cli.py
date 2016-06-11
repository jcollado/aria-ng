#!/usr/bin/env python

from aria import *
from aria.reader import *
from aria.parser import *
from aria.consumer import *
from aria.presenter import *
from tosca.datatypes import *

from clint.arguments import Args 
from clint.textui import puts, colored, indent

def show_help():
    puts(colored.red('ARIA CLI'))
    with indent(2):
        puts('aria [profile URI or file path]')

if __name__ == '__main__':
    args = Args()
    
    if len(args.all) == 0:
        show_help()
        exit(1)
    
    uri = args.all[0]

    #reader = YamlReader('simple-blueprint.yaml')
    #reader.read()

    #r = Credential({'properties': {'protocol': 'http'}})
    #print r.properties.protocol

    parser = DefaultParser(uri)
    presentation = parser.parse()

    #Writer(structure).consume()

    validator = Validator(presentation)
    validator.consume()
    
    #print presentation.profile.tosca_definitions_version

    Printer(presentation).consume()

