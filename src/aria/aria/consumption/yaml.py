
from ..reading import init_yaml
from .consumer import Consumer
from .exceptions import ConsumerError
import ruamel.yaml as yaml # @UnresolvedImport

class Yaml(Consumer):
    """
    ARIA YAML writer.
    
    Outputs the presentation's raw data as YAML text.
    """
    
    def consume(self):
        try:
            init_yaml()
            text = yaml.dump(self.context.presentation._raw, Dumper=yaml.RoundTripDumper)
            self.context.out.write(text)
        except Exception as e:
            raise ConsumerError('YamlWriter: %s' % e, cause=e)
