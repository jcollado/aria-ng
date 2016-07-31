
from .consumer import Consumer

class Validate(Consumer):
    """
    Validates the presentation.
    """

    def consume(self):
        self.context.presentation._validate(self.context)
