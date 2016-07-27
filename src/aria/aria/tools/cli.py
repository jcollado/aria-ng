
from .. import install_aria_extensions, print_exception, import_fullname
from ..consumption import ConsumptionContext
from .utils import CommonArgumentParser, create_parser_ns

class ArgumentParser(CommonArgumentParser):
    def __init__(self):
        super(ArgumentParser, self).__init__(description='CLI', prog='aria')
        self.add_argument('uri', help='URI or file path to profile')
        self.add_argument('consumer', nargs='?', default='aria.consumption.Print', help='consumer class')

def main():
    try:
        args, unknown_args = ArgumentParser().parse_known_args()
        
        consumer_class_name = args.consumer
        if '.' not in consumer_class_name:
            consumer_class_name = consumer_class_name.title()
        
        install_aria_extensions()

        consumer_class = import_fullname(consumer_class_name, ['aria.consumption'])
        parser = create_parser_ns(args)

        context = ConsumptionContext()
        context.args = unknown_args
        
        parser.parse_and_validate(context)
        
        if context.validation.dump_issues():
            exit(0)

        consumer_class(context).consume()
    except Exception as e:
        print_exception(e)

if __name__ == '__main__':
    main()
