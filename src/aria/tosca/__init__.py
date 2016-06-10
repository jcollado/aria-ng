
from primitives import *
from profile import *

class PropertyFilter(object):
    """
    A property filter definition defines criteria, using constraint clauses, for selection of a TOSCA entity based upon it property values.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_PROPERTY_FILTER_DEFN>`
    """
    
    DESCRIPTION = 'A property filter definition defines criteria, using constraint clauses, for selection of a TOSCA entity based upon it property values.'

class Artifact(object):
    """
    An artifact definition defines a named, typed file that can be associated with Node Type or Node Template and used by orchestration engine to facilitate deployment and implementation of interface operations.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_ARTIFACT_DEF>`
    """

    def __init__(self, structure={}):
        self.structure = structure

    @property
    def type(self):
        return self.structure.get('type')
        
    @type.setter
    def type(self, value):
        self.structure['type'] = value

    @property
    def file(self):
        return self.structure.get('file')

    @file.setter
    def file(self, value):
        self.structure['file'] = value

    @property
    def repository(self):
        return self.structure.get('repository')

    @repository.setter
    def repository(self, value):
        self.structure['repository'] = value

    @property
    def description(self):
        return self.structure.get('description')

    @description.setter
    def description(self, value):
        self.structure['description'] = value

    @property
    def deploy_path(self):
        return self.structure.get('deploy_path')

    @deploy_path.setter
    def deploy_path(self, value):
        self.structure['deploy_path'] = value
