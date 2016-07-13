
#from .definitions import PropertyDefinition, CapabilityDefinition
from aria import dsl_specification
from aria.presentation import Presentation, has_fields, object_sequenced_list_field

@has_fields
@dsl_specification('3.5.4', 'tosca-simple-profile-1.0')
class NodeFilter(Presentation):
    """
    A node filter definition defines criteria for selection of a TOSCA Node Template based upon the template's property values, capabilities and capability properties.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_NODE_FILTER_DEFN>`__
    """

    #@object_sequenced_list_field(PropertyDefinition)
    def properties(self):
        """
        An optional sequenced list of property filters that would be used to select (filter) matching TOSCA entities (e.g., Node Template, Node Type, Capability Types, etc.) based upon their property definitions' values.
        
        :rtype: list of (str, :class:`PropertyDefinition`)
        """

    #@object_sequenced_list_field(CapabilityDefinition)
    def capabilities(self):
        """
        An optional sequenced list of property filters that would be used to select (filter) matching TOSCA entities (e.g., Node Template, Node Type, Capability Types, etc.) based upon their capabilities' property definitions' values.
        
        :rtype: list of (str, :class:`CapabilityDefinition`)
        """

@has_fields
@dsl_specification('3.5.3', 'tosca-simple-profile-1.0')
class PropertyFilter(Presentation):
    """
    A property filter definition defines criteria, using constraint clauses, for selection of a TOSCA entity based upon it property values.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_PROPERTY_FILTER_DEFN>`__
    """

    # TODO
