
#from aria.consumption import Implementer

def prepare_deployment_plan(plan, inputs=None, **kwargs):
    """
    Prepare a plan for deployment
    """
    #print '!!! prepare_deployment_plan'
    #print plan
    #print inputs
    #print kwargs
    
    #implementer = Implementer(plan)
    #implementer.implement()
    #service = implementer.service
    #node_instances = [create_node_instance(name, getattr(service, name)) for name in service.context.nodes]
    
    return plan.deployment_plan.as_dict
