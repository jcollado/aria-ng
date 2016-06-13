
from consumer import Consumer

class Validator(Consumer):
    """
    ARIA validator.
    
    Validates the presentation.
    """

    def consume(self):
        self.validate()
    
    def validate(self):
        issues = []
        self.presentation.validate(issues)
        return issues
