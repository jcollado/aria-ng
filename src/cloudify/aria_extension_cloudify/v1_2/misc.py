
from aria import dsl_specification
from aria.presentation import Presentation, has_fields, primitive_field

@has_fields
@dsl_specification('node-templates', 'cloudify-1.2')
class Instances(Presentation):
    """
    The instances key is used for configuring the deployment characteristics of the node template.
    
    See the `Cloudify DSL v1.2 specification <http://docs.getcloudify.org/3.3.1/blueprints/spec-node-templates/>`__.
    """
    
    @primitive_field(int, default=1)
    def deploy(self):
        """
        The number of node-instances this node template will have.
        
        :rtype: int
        """
