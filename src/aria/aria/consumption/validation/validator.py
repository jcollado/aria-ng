
from ..consumer import Consumer

class Validator(Consumer):
    """
    ARIA validator.
    
    Validates the presentation.
    """

    def consume(self):
        self.context.presentation._validate(self.context)
