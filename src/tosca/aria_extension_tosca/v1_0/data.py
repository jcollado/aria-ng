
from aria import dsl_specification

YAML_TO_PYTHON = {
    # YAML 1.2:
    'tag:yaml.org,2002:str': str,
    'tag:yaml.org,2002:integer': int,
    'tag:yaml.org,2002:float': float,
    'tag:yaml.org,2002:bool': bool,
    # TOSCA aliases:
    'string': str,
    'integer': int,
    'float': float,
    'boolean': bool
}

@dsl_specification('3.3.1', 'tosca-simple-profile-1.0')
def get_class_for_data_type(the_type):
    """
    Many of the types we use in this profile are built-in types from the YAML 1.2 specification (i.e., those identified by the "tag:yaml.org,2002" version tag) [YAML-1.2].
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc373867862>`__
    """
    if the_type is None:
        return str
    return YAML_TO_PYTHON.get(the_type)
