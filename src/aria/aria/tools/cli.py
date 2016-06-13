
from aria import print_exception, import_class
from aria.consumer import Validator
from clint.textui import puts, colored, indent
from utils import CommonArgumentParser, create_parser_ns

class ArgumentParser(CommonArgumentParser):
    def __init__(self):
        super(ArgumentParser, self).__init__(description='CLI', prog='aria')
        self.add_argument('uri', help='URI or file path to profile')
        self.add_argument('consumer', nargs='?', default='aria.consumer.Printer', help='consumer class')

def main():
    try:
        args, unknown_args = ArgumentParser().parse_known_args()
        
        consumer_class = import_class(args.consumer, ['aria.consumer'])
        
        parser = create_parser_ns(args)
        presentation, issues = parser.validate()
        
        if issues:
            for issue in issues:
                puts(colored.red('%s' % issue))
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
