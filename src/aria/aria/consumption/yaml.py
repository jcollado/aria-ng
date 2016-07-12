
from .consumer import Consumer
from .exceptions import ConsumerError
import ruamel.yaml as yaml # @UnresolvedImport

class YamlWriter(Consumer):
    """
    ARIA YAML writer.
    
    Outputs the presentation's raw data as YAML text.
    """
    
    def consume(self):
        try:
            text = yaml.dump(self.context.presentation.raw, Dumper=yaml.RoundTripDumper)
            self.context.out.write(text)
        except Exception as e:
            raise ConsumerError('YamlWriter: %s' % e, cause=e)
