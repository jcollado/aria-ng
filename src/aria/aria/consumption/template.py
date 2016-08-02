
from .consumer import Consumer

class Template(Consumer):
    """
    Emits the deployment template derived from the presentation.
    """

    def consume(self):
        deployment_template = self.deployment_template
        if deployment_template is not None:
            deployment_template.dump(self.context)
    
    @property
    def deployment_template(self):
        deployment_template = self.context.presentation._get_deployment_template(self.context)
        deployment_template.link(self.context)
        return deployment_template if not self.context.validation.issues else None
