
from .consumer import Consumer

class Presentation(Consumer):
    """
    Emits the complete presentation of the blueprint.
    """
    
    def consume(self):
        self.context.presentation._dump(self.context)
