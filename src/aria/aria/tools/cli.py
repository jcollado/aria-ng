#!/usr/bin/env python

from aria import VERSION, import_class, print_exception
from aria.consumer import Validator
from argparse import ArgumentParser
from clint.textui import puts, colored, indent

class Arguments(ArgumentParser):
    def __init__(self):
        super(Arguments, self).__init__(description='ARIA version %s' % VERSION, prog='aria')
        self.add_argument('uri', help='URI or file path to profile')
        self.add_argument('consumer', nargs='?', default='aria.consumer.Printer', help='consumer class')
        self.add_argument('--parser', default='aria.parser.DefaultParser', help='parser class')
        self.add_argument('--loader-source', default='aria.loader.DefaultLoaderSource', help='loader source class for the parser')
        self.add_argument('--reader-source', default='aria.reader.DefaultReaderSource', help='reader source class for the parser')
        self.add_argument('--presenter-source', default='aria.presenter.DefaultPresenterSource', help='presenter source class for the parser')
        self.add_argument('--presenter', help='force use of this presenter class in parser')

def main():
    try:
        arguments, unknown_args = Arguments().parse_known_args()
        
        uri = arguments.uri
        consumer_class = import_class(arguments.consumer, ['aria.consumer'])
        parser_class = import_class(arguments.parser, ['aria.parser'])
        loader_source_class = import_class(arguments.loader_source, ['aria.loader'])
        reader_source_class = import_class(arguments.reader_source, ['aria.reader'])
        presenter_source_class = import_class(arguments.presenter_source, ['aria.presenter'])
        presenter_class = import_class(arguments.presenter, ['aria.presenter'])
        
        parser = parser_class(locator=uri,
            loader_source=loader_source_class(),
            reader_source=reader_source_class(),
            presenter_source=presenter_source_class(),
            presenter_class=presenter_class)
        
        presentation = parser.parse()
        
        if Validator(presentation).validate():
            exit(0)

        #presentation.profile.description = 12
        #print presentation.profile.description
        
        consumer_class(presentation, unknown_args).consume()

        #reader = YamlReader('simple-blueprint.yaml')
        #reader.read()

        #r = Credential({'properties': {'protocol': 'http'}})
        #print r.properties.protocol

        #Writer(structure).consume()
    except Exception as e:
        print_exception(e)

if __name__ == '__main__':
    main()
