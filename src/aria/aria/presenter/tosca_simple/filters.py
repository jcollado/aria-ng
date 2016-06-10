
from base import Base
from definitions import *

class NodeFilter(Base):
    """
    A node filter definition defines criteria for selection of a TOSCA Node Template based upon the template's property values, capabilities and capability properties.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_NODE_FILTER_DEFN>`__
    """

    @property
    def properties(self):
        """
        :class:`PropertyDefinition`
        """
        return self._get_object_list('properties', PropertyDefinition)

    @property
    def capabilities(self):
        """
        :class:`CapabilityDefinition`
        """
        return self._get_object_list('capabilities', CapabilityDefinition)

class PropertyFilter(Base):
    """
    A property filter definition defines criteria, using constraint clauses, for selection of a TOSCA entity based upon it property values.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_PROPERTY_FILTER_DEFN>`__
    """

    # TODO
