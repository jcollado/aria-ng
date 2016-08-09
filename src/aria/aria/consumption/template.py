
from .consumer import Consumer

class Template(Consumer):
    """
    Emits the deployment template derived from the presentation.
    """

    def consume(self):
        self.create_deployment_template()
        if not self.context.validation.has_issues:
            if '--types' in self.context.args:
                self.context.deployment.dump_types(self.context)
            else:
                self.context.deployment.template.dump(self.context)
    
    def create_deployment_template(self):
        if hasattr(self.context.presentation, '_get_deployment_template'):
            self.context.deployment.template = self.context.presentation._get_deployment_template(self.context)
            if self.context.deployment.template is not None:
                self.context.deployment.template.validate(self.context)
