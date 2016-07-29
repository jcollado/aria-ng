
from ..deployment import Deployment
from .consumer import Consumer

class Deploy(Consumer):
    """
    ARIA deployer.
    
    Created a deployment plan for the presentation.
    """

    def consume(self):
        deployment = self.deployment
        deployment.dump(self.context)
        deployment.link(self.context)
    
    @property
    def deployment(self):
        deployment = Deployment()
        
        if self.context.presentation.node_templates:
            for node_template_name, node_template in self.context.presentation.node_templates.iteritems():
                deployment.node_templates[node_template_name] = node_template._get_deployment(self.context)

        return deployment
