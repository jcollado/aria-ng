
from .. import install_aria_extensions, print_exception, import_modules, DSL_SPECIFICATION_PACKAGES, DSL_SPECIFICATION, iter_spec
from .utils import BaseArgumentParser
from clint.textui import puts, colored, indent
import csv, sys

class ArgumentParser(BaseArgumentParser):
    def __init__(self):
        super(ArgumentParser, self).__init__(description='Specification Tool', prog='aria-spec')
        self.add_argument('--csv', action='store_true', help='output as CSV')

def main():
    try:
        args, _ = ArgumentParser().parse_known_args()

        install_aria_extensions()
        
        # Make sure that all @dsl_specification decorators are processed
        for p in DSL_SPECIFICATION_PACKAGES:
            import_modules(p)

        if args.csv:
            w = csv.writer(sys.stdout, quoting=csv.QUOTE_ALL)
            w.writerow(('Specification', 'Section', 'Code', 'URL'))
            for spec in sorted(DSL_SPECIFICATION):
                for section, details in iter_spec(spec):
                    w.writerow((spec, section, details['code'], details['url']))
        
        else:
            for spec in sorted(DSL_SPECIFICATION):
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
