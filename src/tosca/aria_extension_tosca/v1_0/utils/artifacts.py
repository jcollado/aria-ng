
from collections import OrderedDict

#
# NodeType, NodeTemplate
#

def get_inherited_artifact_definitions(context, presentation, for_presentation=None):
    
    if hasattr(presentation, '_get_type'):
        # In NodeTemplate
        parent = presentation._get_type(context)
    else:
        # In NodeType
        parent = presentation._get_parent(context)
    
    # Get artifact definitions from parent
    artifacts = get_inherited_artifact_definitions(context, parent, for_presentation=presentation) if parent is not None else OrderedDict()
    
    # Add/override our artifact definitions
    our_artifacts = presentation.artifacts
    if our_artifacts:
        for artifact_name, artifact in our_artifacts.iteritems():
            artifacts[artifact_name] = artifact._clone(for_presentation)
    
    return artifacts