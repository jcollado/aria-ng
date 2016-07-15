
from aria.presentation import Presentation, has_fields, primitive_field

@has_fields
class ToscaPresentation(Presentation):
    @primitive_field()
    def _extensions(self):
        pass

