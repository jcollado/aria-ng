
from aria import tosca_specification
from aria import has_fields
from aria.presenter import Presentation

@has_fields
@tosca_specification('3.5.9')
class PropertyAssignment(Presentation):
    """
    This section defines the grammar for assigning values to named properties within TOSCA Node and Relationship templates that are defined in their corresponding named types.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_PROPERTY_VALUE_ASSIGNMENT>`__
    """
    
    @property
    def value(self):
        return self.raw
    
    @value.setter
    def value(self, value):
        self.raw = value
        
    #TODO

@has_fields
@tosca_specification('3.7.2')
class RequirementAssignment(Presentation):
    """
    A Requirement assignment allows template authors to provide either concrete names of TOSCA templates or provide abstract selection criteria for providers to use to find matching TOSCA templates that are used to fulfill a named requirement's declared TOSCA Node Type.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_REQUIREMENT_ASSIGNMENT>`__
    """
    
    #TODO

@has_fields
@tosca_specification('3.7.1')
class CapabilityAssignment(Presentation):
    """
    A capability assignment allows node template authors to assign values to properties and attributes for a named capability definition that is part of a Node Template's type definition.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_CAPABILITY_ASSIGNMENT>`__
    """
    
    #TODO

@has_fields
@tosca_specification('3.5.11')
class AttributeAssignment(Presentation):
    """
    This section defines the grammar for assigning values to named attributes within TOSCA Node and Relationship templates which are defined in their corresponding named types.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_ATTRIBUTE_VALUE_ASSIGNMENT>`__
    """
    
    #TODO
