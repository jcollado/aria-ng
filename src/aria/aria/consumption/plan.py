
from .template import Template

class Plan(Template):
    """
    Emits the deployment plan instantiated from the deployment template.
    """

    def consume(self):
        topology = self.topology
        topology.link(self.context)
        if self.context.validation.issues:
            return
        topology.dump(self.context)
