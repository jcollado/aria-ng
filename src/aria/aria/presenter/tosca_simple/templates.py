
from aria.presenter import HasRaw, has_properties, property_primitive, property_primitive_list, property_object_dict, required
from definitions import ParameterDefinition, GroupDefinition, PolicyDefinition, ParameterDefinition, InterfaceDefinition, ArtifactDefinition
from assignments import PropertyAssignment, AttributeAssignment, RequirementAssignment, CapabilityAssignment
from filters import NodeFilter

@has_properties
class NodeTemplate(HasRaw):
    """
    A Node Template specifies the occurrence of a manageable software component as part of an application's topology model which is defined in a TOSCA Service Template. A Node template is an instance of a specified Node Type and can provide customized properties, constraints or operations which override the defaults provided by its Node Type and its implementations.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_NODE_TEMPLATE>`__
    """

    @required
    @property_primitive
    def type(self):
        pass

    @property_primitive
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @property_primitive_list
    def directives(self):
        pass

    @property_object_dict(PropertyAssignment)
    def properties(self):
        """
        :class:`PropertyAssignment`
        """

    @property_object_dict(AttributeAssignment)
    def attributes(self):
        """
        :class:`AttributeAssignment`
        """

    @property_object_dict(RequirementAssignment)
    def requirements(self):
        """
        :class:`RequirementAssignment`
        """

    @property_object_dict(CapabilityAssignment)
    def capabilities(self):
        """
        :class:`CapabilityAssignment`
        """

    @property_object_dict(InterfaceDefinition)
    def interfaces(self):
        """
        :class:`InterfaceDefinition`
        """

    @property_object_dict(ArtifactDefinition)
    def artifacts(self):
        """
        :class:`ArtifactDefinition`
        """

    @property_object_dict(NodeFilter)
    def node_filter(self):
        """
        :class:`NodeFilter`
        """

    @property_primitive
    def copy(self):
        pass

@has_properties
class RelationshipTemplate(HasRaw):
    """
    A Relationship Template specifies the occurrence of a manageable relationship between node templates as part of an application's topology model that is defined in a TOSCA Service Template. A Relationship template is an instance of a specified Relationship Type and can provide customized properties, constraints or operations which override the defaults provided by its Relationship Type and its implementations.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_RELATIONSHIP_TEMPLATE>`__
    """

    @required
    @property_primitive
    def type(self):
        pass

    @property_primitive
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @property_object_dict(PropertyAssignment)
    def properties(self):
        """
        :class:`PropertyAssignment`
        """

    @property_object_dict(AttributeAssignment)
    def attributes(self):
        """
        :class:`AttributeAssignment`
        """

    @property_object_dict(InterfaceDefinition)
    def interfaces(self):
        """
        :class:`InterfaceDefinition`
        """

    @property_primitive
    def copy(self):
        pass

    @property_primitive_list
    def targets(self):
        pass

@has_properties
class TopologyTemplate(HasRaw):
    """
    This section defines the topology template of a cloud application. The main ingredients of the topology template are node templates representing components of the application and relationship templates representing links between the components. These elements are defined in the nested node_templates section and the nested relationship_templates sections, respectively. Furthermore, a topology template allows for defining input parameters, output parameters as well as grouping of node templates.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_TOPOLOGY_TEMPLATE>`__
    """

    @property_primitive
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @property_object_dict(ParameterDefinition)
    def inputs(self):
        """
        :class:`ParameterDefinition`
        """

    @property_object_dict(NodeTemplate)
    def node_templates(self):
        """
        :class:`NodeTemplate`
        """

    @property_object_dict(RelationshipTemplate)
    def relationship_templates(self):
        """
        :class:`RelationshipTemplate`
        """

    @property_object_dict(GroupDefinition)
    def groups(self):
        """
        :class:`GroupDefinition`
        """

    @property_object_dict(PolicyDefinition)
    def policies(self):
        """
        :class:`PolicyDefinition`
        """

    @property_object_dict(ParameterDefinition)
    def outputs(self):
        """
        :class:`ParameterDefinition`
        """
    
    @property
    def substitution_mappings(self):
        return self._get_primitive('substitution_mappings')
