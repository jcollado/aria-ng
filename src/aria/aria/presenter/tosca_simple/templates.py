
from base import Base
from definitions import ParameterDefinition, GroupDefinition, PolicyDefinition, ParameterDefinition, InterfaceDefinition, ArtifactDefinition
from assignments import PropertyAssignment, AttributeAssignment, RequirementAssignment, CapabilityAssignment
from filters import NodeFilter

class TopologyTemplate(Base):
    """
    This section defines the topology template of a cloud application. The main ingredients of the topology template are node templates representing components of the application and relationship templates representing links between the components. These elements are defined in the nested node_templates section and the nested relationship_templates sections, respectively. Furthermore, a topology template allows for defining input parameters, output parameters as well as grouping of node templates.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_TOPOLOGY_TEMPLATE>`__
    """

    @property
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
        return self._get_primitive('description')

    @property
    def inputs(self):
        """
        :class:`ParameterDefinition`
        """
        return self._get_object_list('inputs', ParameterDefinition)

    @property
    def node_templates(self):
        """
        :class:`NodeTemplate`
        """
        return self._get_object_dict('node_templates', NodeTemplate)

    @property
    def relationship_templates(self):
        """
        :class:`RelationshipTemplate`
        """
        return self._get_object_list('relationship_templates', RelationshipTemplate)

    @property
    def groups(self):
        """
        :class:`GroupDefinition`
        """
        return self._get_object_list('groups', GroupDefinition)

    @property
    def policies(self):
        """
        :class:`PolicyDefinition`
        """
        return self._get_object_list('policies', PolicyDefinition)

    @property
    def outputs(self):
        """
        :class:`ParameterDefinition`
        """
        return self._get_object_list('outputs', ParameterDefinition)
    
    @property
    def substitution_mappings(self):
        return self._get_primitive('substitution_mappings')

class NodeTemplate(Base):
    """
    A Node Template specifies the occurrence of a manageable software component as part of an application's topology model which is defined in a TOSCA Service Template. A Node template is an instance of a specified Node Type and can provide customized properties, constraints or operations which override the defaults provided by its Node Type and its implementations.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_NODE_TEMPLATE>`__
    """

    REQUIRED = ['type']

    @property
    def type(self):
        return self._get_primitive('type')

    @property
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
        return self._get_primitive('description')

    @property
    def directives(self):
        return self._get_primitive_list('directives')

    @property
    def properties(self):
        """
        :class:`PropertyAssignment`
        """
        return self._get_object_list('properties', PropertyAssignment)

    @property
    def attributes(self):
        """
        :class:`AttributeAssignment`
        """
        return self._get_object_list('attributes', AttributeAssignment)

    @property
    def requirements(self):
        """
        :class:`RequirementAssignment`
        """
        return self._get_object_list('requirements', RequirementAssignment)

    @property
    def capabilities(self):
        """
        :class:`CapabilityAssignment`
        """
        return self._get_object_list('capabilities', CapabilityAssignment)

    @property
    def interfaces(self):
        """
        :class:`InterfaceDefinition`
        """
        return self._get_object_list('interfaces', InterfaceDefinition)

    @property
    def artifacts(self):
        """
        :class:`ArtifactDefinition`
        """
        return self._get_object_list('artifacts', ArtifactDefinition)

    @property
    def node_filter(self):
        """
        :class:`NodeFilter`
        """
        return self._get_object('node_filter', NodeFilter)

    @property
    def copy(self):
        return self._get_primitive('copy')

class RelationshipTemplate(Base):
    """
    A Relationship Template specifies the occurrence of a manageable relationship between node templates as part of an application's topology model that is defined in a TOSCA Service Template. A Relationship template is an instance of a specified Relationship Type and can provide customized properties, constraints or operations which override the defaults provided by its Relationship Type and its implementations.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_RELATIONSHIP_TEMPLATE>`__
    """

    REQUIRED = ['type']

    @property
    def type(self):
        return self._get_primitive('type')

    @property
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """
        return self._get_primitive('description')

    @property
    def properties(self):
        """
        :class:`PropertyAssignment`
        """
        return self._get_object_list('properties', PropertyAssignment)

    @property
    def attributes(self):
        """
        :class:`AttributeAssignment`
        """
        return self._get_object_list('attributes', AttributeAssignment)

    @property
    def interfaces(self):
        """
        :class:`InterfaceDefinition`
        """
        return self._get_object_list('interfaces', InterfaceDefinition)

    @property
    def copy(self):
        return self._get_primitive('copy')

        return self._get_primitive_list('targets')
