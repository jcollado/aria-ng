
from .. import VERSION, import_class
from argparse import ArgumentParser

class BaseArgumentParser(ArgumentParser):
    def __init__(self, description, **kwargs):
        super(BaseArgumentParser, self).__init__(description='ARIA version %s %s' % (VERSION, description), **kwargs)

class CommonArgumentParser(BaseArgumentParser):
    def __init__(self, description, **kwargs):
        super(CommonArgumentParser, self).__init__(description='ARIA version %s %s' % (VERSION, description), **kwargs)
        self.add_argument('--parser', default='aria.parser.DefaultParser', help='parser class')
        self.add_argument('--loader-source', default='aria.loader.DefaultLoaderSource', help='loader source class for the parser')
        self.add_argument('--reader-source', default='aria.reader.DefaultReaderSource', help='reader source class for the parser')
        self.add_argument('--presenter-source', default='aria.presenter.DefaultPresenterSource', help='presenter source class for the parser')
        self.add_argument('--presenter', help='force use of this presenter class in parser')

def create_parser_ns(ns, **kwargs):
    args = vars(ns).copy()
    args.update(kwargs)
    return create_parser(**args)

def create_parser(uri, parser, loader_source, reader_source, presenter_source, presenter, **kwargs):
    parser_class = import_class(parser, ['aria.parser'])
    loader_source_class = import_class(loader_source, ['aria.loader'])
    reader_source_class = import_class(reader_source, ['aria.reader'])
    presenter_source_class = import_class(presenter_source, ['aria.presenter'])
    presenter_class = import_class(presenter, ['aria.presenter'])

    return parser_class(location=uri,
        loader_source=loader_source_class(),
        reader_source=reader_source_class(),
        presenter_source=presenter_source_class(),
        presenter_class=presenter_class)
