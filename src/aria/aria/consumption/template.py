
from .consumer import Consumer

class Template(Consumer):
    """
    Emits the deployment template derived from the presentation.
    """

    def consume(self):
        topology = self.topology
        topology.link(self.context)
        if self.context.validation.dump_issues():
            return
        topology.dump(self.context)
    
    @property
    def topology(self):
        return self.context.presentation._get_topology(self.context)
