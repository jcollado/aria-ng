
from ... import has_fields
from ..tosca import InterfaceDefinition as BaseInterfaceDefinition
from .misc import Operation

@has_fields
class InterfaceDefinition(BaseInterfaceDefinition):
    @property
    def operations(self):
        """
        :rtype: dict of str, :class:`Operation`
        """
        return {k: Operation(v) for k, v in self.raw.iteritems()}
