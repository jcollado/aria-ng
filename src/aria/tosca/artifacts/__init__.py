
from aria import has_validated_properties, validated_property, property_type, property_default, property_status, required_property
import tosca

@has_validated_properties
class Root(object):
    """
    This is the default (root) TOSCA Artifact Type definition that all other TOSCA base Artifact Types derive from.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_ARTIFACTS_ROOT>`__
    """

@has_validated_properties
class File(Root):
    """
    This artifact type is used when an artifact definition needs to have its associated file simply treated as a file and no special handling/handlers are invoked (i.e., it is not treated as either an implementation or deployment artifact type).
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#>`__ (no anchor)
    """

    SHORTHAND_NAME = 'File'
    TYPE_QUALIFIED_NAME = 'tosca:File'
    TYPE_URI = 'tosca.artifacts.File'

@has_validated_properties
class Deployment(Root):
    """
    This artifact type represents the parent type for all deployment artifacts in TOSCA. This class of artifacts typically represents a binary packaging of an application or service that is used to install/create or deploy it as part of a node's lifecycle.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_ARTIFACTS_DEPLOYMENT>`__
    """
    
    SHORTHAND_NAME = 'Deployment'
    TYPE_QUALIFIED_NAME = 'tosca:Deployment'
    TYPE_URI = 'tosca.artifacts.Deployment'

@has_validated_properties
class Image(Deployment):
    """
    This artifact type represents a parent type for any "image" which is an opaque packaging of a TOSCA Node's deployment (whether real or virtual) whose contents are typically already installed and pre-configured (i.e., "stateful") and prepared to be run on a known target container.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_ARTIFACTS_DEPLOYMENT_IMAGE>`__
    """
    
    SHORTHAND_NAME = 'Deployment.Image'
    TYPE_QUALIFIED_NAME = 'tosca:Deployment.Image'
    TYPE_URI = 'tosca.artifacts.Deployment.Image'

Deployment.Image = Image

@has_validated_properties
class VM(Deployment):
    """
    This artifact represents the parent type for all Virtual Machine (VM) image and container formatted deployment artifacts. These images contain a stateful capture of a machine (e.g., server) including operating system and installed software along with any configurations and can be run on another machine using a hypervisor which virtualizes typical server (i.e., hardware) resources.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_ARTIFACTS_DEPLOY_IMAGE_VM>`__
    """
    
    SHORTHAND_NAME = 'Deployment.Image.VM'
    TYPE_QUALIFIED_NAME = 'tosca:Deployment.Image.VM'
    TYPE_URI = 'tosca.artifacts.Deployment.Image.VM'

Deployment.Image.VM = VM

@has_validated_properties
class Implementation(Root):
    """
    This artifact type represents the parent type for all implementation artifacts in TOSCA. These artifacts are used to implement operations of TOSCA interfaces either directly (e.g., scripts) or indirectly (e.g., config. files).
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_ARTIFACTS_IMPLEMENTATION>`__
    """
    
    SHORTHAND_NAME = 'Implementation'
    TYPE_QUALIFIED_NAME = 'tosca:Implementation'
    TYPE_URI = 'tosca.artifacts.Implementation'

@has_validated_properties
class Bash(Implementation):
    """
    This artifact type represents a Bash script type that contains Bash commands that can be executed on the Unix Bash shell.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#>`__ (no anchor)
    """
    
    SHORTHAND_NAME = 'Implementation.Bash'
    TYPE_QUALIFIED_NAME = 'tosca:Implementation.Bash'
    TYPE_URI = 'tosca.artifacts.Implementation.Bash'

    MIME_TYPE = 'application/x-sh'
    FILE_EXT = ['sh']

Implementation.Bash = Bash

@has_validated_properties
class Python(Implementation):
    """
    This artifact type represents a Python file that contains Python language constructs that can be executed within a Python interpreter.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#>`__ (no anchor)
    """
    
    SHORTHAND_NAME = 'Implementation.Python'
    TYPE_QUALIFIED_NAME = 'tosca:Implementation.Python'
    TYPE_URI = 'tosca.artifacts.Implementation.Python'

    MIME_TYPE = 'application/x-python'
    FILE_EXT = ['py']

Implementation.Python = Python
