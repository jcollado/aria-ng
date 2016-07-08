
from .... import dsl_specification
from ... import Presentation, has_fields

@has_fields
@dsl_specification('3.5.9', 'tosca-simple-profile-1.0')
class PropertyAssignment(Presentation):
    """
    This section defines the grammar for assigning values to named properties within TOSCA Node and Relationship templates that are defined in their corresponding named types.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_PROPERTY_VALUE_ASSIGNMENT>`__
    """

    def __init__(self, *args, **kwargs):
        super(PropertyAssignment, self).__init__(*args, **kwargs)
        self._allow_unknown_fields = True
    
    @property
    def value(self):
        return self._raw
    
    @value.setter
    def value(self, value):
        self._raw = value
        
    #TODO

@has_fields
@dsl_specification('3.7.2', 'tosca-simple-profile-1.0')
class RequirementAssignment(Presentation):
    """
    A Requirement assignment allows template authors to provide either concrete names of TOSCA templates or provide abstract selection criteria for providers to use to find matching TOSCA templates that are used to fulfill a named requirement's declared TOSCA Node Type.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_REQUIREMENT_ASSIGNMENT>`__
    """
    
    #TODO

@has_fields
@dsl_specification('3.7.1', 'tosca-simple-profile-1.0')
class CapabilityAssignment(Presentation):
    """
    A capability assignment allows node template authors to assign values to properties and attributes for a named capability definition that is part of a Node Template's type definition.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_CAPABILITY_ASSIGNMENT>`__
    """
    
    #TODO

@has_fields
@dsl_specification('3.5.11', 'tosca-simple-profile-1.0')
class AttributeAssignment(Presentation):
    """
    This section defines the grammar for assigning values to named attributes within TOSCA Node and Relationship templates which are defined in their corresponding named types.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_ATTRIBUTE_VALUE_ASSIGNMENT>`__
    """
    
    #TODO
