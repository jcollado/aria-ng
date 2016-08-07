
from .template import Template

class Plan(Template):
    """
    Emits the deployment plan instantiated from the deployment template.
    """

    def consume(self):
        self.create_deployment_plan()
        if (self.context.deployment.plan is not None) and (not self.context.validation.has_issues):
            if '--graph' in self.context.args:
                self.context.deployment.plan.dump_graph(self.context)
            elif '--json' in self.context.args:
                print self.context.deployment.get_plan_as_json(indent=2)
            else:
                self.context.deployment.plan.dump(self.context)

    def create_deployment_plan(self):
        self.create_deployment_template()
        if self.context.deployment.template is not None:
            if not self.context.validation.has_issues:
                self.context.deployment.template.instantiate(self.context, None)
            if not self.context.validation.has_issues:
                self.context.deployment.plan.validate(self.context)
            if not self.context.validation.has_issues:
                self.context.deployment.plan.satisfy_requirements(self.context)
            if not self.context.validation.has_issues:
                self.context.deployment.plan.validate_capabilities(self.context)
