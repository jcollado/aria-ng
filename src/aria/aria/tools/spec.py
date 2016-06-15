
from .. import import_modules, print_exception, TOSCA_SPECIFICATION, iter_spec
from .utils import BaseArgumentParser
from clint.textui import puts, colored, indent
import csv, sys, pkgutil

class ArgumentParser(BaseArgumentParser):
    def __init__(self):
        super(ArgumentParser, self).__init__(description='Spec', prog='aria-spec')
        self.add_argument('--csv', action='store_true', help='output as CSV')

def main():
    try:
        args, unknown_args = ArgumentParser().parse_known_args()

        # By importing all modules, we will make sure that their classes are defined
        # and that TOSCA_SPECIFICATION gets properly filled.
        import_modules('aria')
        import_modules('tosca')

        if args.csv:
            w = csv.writer(sys.stdout, quoting=csv.QUOTE_ALL)
            w.writerow(('Specification', 'Section', 'Code', 'URL'))
            for spec in TOSCA_SPECIFICATION:
                for section, details in iter_spec(spec):
                    w.writerow((spec, section, details['code'], details['url']))
        
        else:
            for spec in TOSCA_SPECIFICATION:
                puts(colored.cyan(spec))
                with indent(2):
                    for section, details in iter_spec(spec):
                        puts(colored.blue(section))
                        with indent(2):
                            for k, v in details.iteritems():
                                puts('%s: %s' % (colored.magenta(k), v))
        
    except Exception as e:
        print_exception(e)

if __name__ == '__main__':
    main()
