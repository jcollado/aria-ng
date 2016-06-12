
from consumer import Consumer
from exceptions import ConsumerError
import ruamel.yaml as yaml
import sys

class YamlWriter(Consumer):
    """
    ARIA YAML writer.
    
    Outputs the presentation's raw data as YAML text.
    """
    
    def __init__(self, presentation, args=[], out=sys.stdout):
        super(YamlWriter, self).__init__(presentation, args)
        self.out = out
        
    def consume(self):
        try:
            text = yaml.dump(self.presentation.raw, Dumper=yaml.RoundTripDumper)
            self.out.write(text)
        except Exception as e:
            raise ConsumerError('Writer', e)
