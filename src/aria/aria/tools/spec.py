
from aria import print_exception, TOSCA_SPECIFICATION
from clint.textui import puts, colored, indent
from utils import CommonArgumentParser

class ArgumentParser(CommonArgumentParser):
    def __init__(self):
        super(ArgumentParser, self).__init__(description='Spec', prog='aria-spec')

def main():
    try:
        args, unknown_args = ArgumentParser().parse_known_args()

        import aria.presenter.tosca_simple
        import aria.presenter.cloudify
        import tosca.artifacts
        import tosca.capabilities
        import tosca.capabilities.network
        import tosca.capabilities.nfv
        import tosca.datatypes
        import tosca.datatypes.compute
        import tosca.datatypes.network
        import tosca.groups
        import tosca.groups.nfv
        import tosca.interfaces
        import tosca.interfaces.node
        import tosca.interfaces.node.lifecycle
        import tosca.nodes
        import tosca.nodes.network
        import tosca.nodes.nfv
        import tosca.policies
        import tosca.relationships
        import tosca.relationships.network
        import tosca.relationships.nfv
        
        for spec, sections in TOSCA_SPECIFICATION.iteritems():
            puts(colored.red(spec))
            with indent(2):
                keys = sections.keys()
                def key(value):
                    k = 0.0
                    level = 1.0
                    for part in value.split('-')[0].split('.'):
                        k += float(part) / level
                        level *= 1000.0
                    return k
                keys.sort(key=key)
                for section in keys:
                    details = sections[section]
                    puts(colored.blue(section))
                    with indent(2):
                        for k, v in details.iteritems():
                            puts('%s: %s' % (k, v))
        
    except Exception as e:
        print_exception(e)

if __name__ == '__main__':
    main()
