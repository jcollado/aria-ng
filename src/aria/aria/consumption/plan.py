
from .topology import Topology

class Plan(Topology):
    """
    ARIA deployment plan.
    
    Created a deployment plan for the presentation.
    """

    def consume(self):
        topology = self.topology
        topology.link(self.context)
        if self.context.validation.dump_issues():
            exit(0)
        topology.dump(self.context)
