
from .template import Template

class Plan(Template):
    """
    Emits the deployment plan instantiated from the deployment template.
    """

    def consume(self):
        self.create_deployment_plan()
        if (self.context.deployment.plan is not None) and (not self.context.validation.has_issues):
            self.context.deployment.plan.dump_graph(self.context)
            self.context.deployment.plan.dump(self.context)

    def create_deployment_plan(self):
        self.create_deployment_template()
        if (self.context.deployment.template is not None) and (not self.context.validation.has_issues):
            self.context.deployment.plan = self.context.deployment.template.instantiate(self.context)
            self.context.deployment.plan.satisfy_requirements(self.context)
