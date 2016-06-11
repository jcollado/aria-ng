
from aria.presenter import Presentation, has_fields, primitive_field, primitive_list_field, object_dict_field, required_field
from definitions import ParameterDefinition, GroupDefinition, PolicyDefinition, ParameterDefinition, InterfaceDefinition, ArtifactDefinition
from assignments import PropertyAssignment, AttributeAssignment, RequirementAssignment, CapabilityAssignment
from filters import NodeFilter

@has_fields
class NodeTemplate(Presentation):
    """
    A Node Template specifies the occurrence of a manageable software component as part of an application's topology model which is defined in a TOSCA Service Template. A Node template is an instance of a specified Node Type and can provide customized properties, constraints or operations which override the defaults provided by its Node Type and its implementations.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_NODE_TEMPLATE>`__
    """

    @required_field
    @primitive_field
    def type(self):
        pass

    @primitive_field
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @primitive_list_field
    def directives(self):
        pass

    @object_dict_field(PropertyAssignment)
    def properties(self):
        """
        :class:`PropertyAssignment`
        """

    @object_dict_field(AttributeAssignment)
    def attributes(self):
        """
        :class:`AttributeAssignment`
        """

    @object_dict_field(RequirementAssignment)
    def requirements(self):
        """
        :class:`RequirementAssignment`
        """

    @object_dict_field(CapabilityAssignment)
    def capabilities(self):
        """
        :class:`CapabilityAssignment`
        """

    @object_dict_field(InterfaceDefinition)
    def interfaces(self):
        """
        :class:`InterfaceDefinition`
        """

    @object_dict_field(ArtifactDefinition)
    def artifacts(self):
        """
        :class:`ArtifactDefinition`
        """

    @object_dict_field(NodeFilter)
    def node_filter(self):
        """
        :class:`NodeFilter`
        """

    @primitive_field
    def copy(self):
        pass

@has_fields
class RelationshipTemplate(Presentation):
    """
    A Relationship Template specifies the occurrence of a manageable relationship between node templates as part of an application's topology model that is defined in a TOSCA Service Template. A Relationship template is an instance of a specified Relationship Type and can provide customized properties, constraints or operations which override the defaults provided by its Relationship Type and its implementations.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_RELATIONSHIP_TEMPLATE>`__
    """

    @required_field
    @primitive_field
    def type(self):
        pass

    @primitive_field
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @object_dict_field(PropertyAssignment)
    def properties(self):
        """
        :class:`PropertyAssignment`
        """

    @object_dict_field(AttributeAssignment)
    def attributes(self):
        """
        :class:`AttributeAssignment`
        """

    @object_dict_field(InterfaceDefinition)
    def interfaces(self):
        """
        :class:`InterfaceDefinition`
        """

    @primitive_field
    def copy(self):
        pass

    @primitive_list_field
    def targets(self):
        pass

@has_fields
class TopologyTemplate(Presentation):
    """
    This section defines the topology template of a cloud application. The main ingredients of the topology template are node templates representing components of the application and relationship templates representing links between the components. These elements are defined in the nested node_templates section and the nested relationship_templates sections, respectively. Furthermore, a topology template allows for defining input parameters, output parameters as well as grouping of node templates.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_TOPOLOGY_TEMPLATE>`__
    """

    @primitive_field
    def description(self):
        """
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @object_dict_field(ParameterDefinition)
    def inputs(self):
        """
        :class:`ParameterDefinition`
        """

    @object_dict_field(NodeTemplate)
    def node_templates(self):
        """
        :class:`NodeTemplate`
        """

    @object_dict_field(RelationshipTemplate)
    def relationship_templates(self):
        """
        :class:`RelationshipTemplate`
        """

    @object_dict_field(GroupDefinition)
    def groups(self):
        """
        :class:`GroupDefinition`
        """

    @object_dict_field(PolicyDefinition)
    def policies(self):
        """
        :class:`PolicyDefinition`
        """

    @object_dict_field(ParameterDefinition)
    def outputs(self):
        """
        :class:`ParameterDefinition`
        """
    
    @property
    def substitution_mappings(self):
        return self._get_primitive('substitution_mappings')
