
from aria.presenter import Presentation, has_fields, object_list_field
from definitions import PropertyDefinition, CapabilityDefinition

@has_fields
class NodeFilter(Presentation):
    """
    A node filter definition defines criteria for selection of a TOSCA Node Template based upon the template's property values, capabilities and capability properties.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_NODE_FILTER_DEFN>`__
    """

    @object_list_field(PropertyDefinition)
    def properties(self):
        """
        :class:`PropertyDefinition`
        """

    @object_list_field(CapabilityDefinition)
    def capabilities(self):
        """
        :class:`CapabilityDefinition`
        """

@has_fields
class PropertyFilter(Presentation):
    """
    A property filter definition defines criteria, using constraint clauses, for selection of a TOSCA entity based upon it property values.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_PROPERTY_FILTER_DEFN>`__
    """

    # TODO
