
from .consumer import Consumer

class Deploy(Consumer):
    """
    ARIA deployer.
    
    Created a deployment plan for the presentation.
    """

    def consume(self):
        topology = self.topology
        topology.dump(self.context)
    
    @property
    def topology(self):
        return self.context.presentation._get_topology(self.context)
