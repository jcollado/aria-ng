
from aria.presentation import Presentation, has_fields, primitive_field

@has_fields
class ToscaPresentation(Presentation):
    @primitive_field()
    def _extensions(self):
        pass

    def _get_extension(self, name, default=None):
        extensions = self._extensions
        return extensions.get(name, default) if extensions is not None else None
