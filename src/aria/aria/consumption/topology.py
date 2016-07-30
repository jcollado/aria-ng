
from .consumer import Consumer

class Topology(Consumer):
    """
    ARIA deployment topology.
    
    Created a deployment topology for the presentation.
    """

    def consume(self):
        topology = self.topology
        topology.link(self.context)
        if self.context.validation.dump_issues():
            exit(0)
        topology.dump(self.context)
    
    @property
    def topology(self):
        return self.context.presentation._get_topology(self.context)
