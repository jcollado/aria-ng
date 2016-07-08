
from .... import dsl_specification
from ... import Presentation, has_fields, primitive_field, field_type, field_default

@has_fields
@dsl_specification('node-templates', 'cloudify-1.2')
class Instances(Presentation):
    """
    The instances key is used for configuring the deployment characteristics of the node template.
    
    See the `Cloudify DSL v1.2 specification <http://docs.getcloudify.org/3.3.1/blueprints/spec-node-templates/>`__.
    """
    
    @field_default(1)
    @field_type(int)
    @primitive_field
    def deploy(self):
        """
        The number of node-instances this node template will have.
        
        :rtype: int
        """
