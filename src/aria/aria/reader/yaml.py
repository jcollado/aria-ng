
from reader import Reader
from exceptions import ReaderError
import ruamel.yaml as yaml

class YamlReader(Reader):
    """
    ARIA YAML reader.
    """
    
    def read(self):
        data = self.load()
        try:
            return yaml.load(data, yaml.RoundTripLoader)
        except e:
            raise ReaderError('YAML', e)
