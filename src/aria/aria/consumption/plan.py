
from .template import Template

class Plan(Template):
    """
    Emits the deployment plan instantiated from the deployment template.
    """

    def consume(self):
        deployment_template = self.deployment_template
        if deployment_template is not None:
            plan = deployment_template.instantiate()
            plan.dump(self.context)
