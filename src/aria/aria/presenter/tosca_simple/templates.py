
from aria.presenter import Presentation, has_fields, primitive_field, primitive_list_field, object_dict_field, field_type, required_field
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
    @field_type(str)
    @primitive_field
    def type(self):
        """
        The required name of the Node Type the Node Template is based upon.
        """

    @field_type(str)
    @primitive_field
    def description(self):
        """
        An optional description for the Node Template.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @field_type(str)
    @primitive_list_field
    def directives(self):
        """
        An optional list of directive values to provide processing instructions to orchestrators and tooling.
        """

    @object_dict_field(PropertyAssignment)
    def properties(self):
        """
        An optional list of property value assignments for the Node Template.
        
        :class:`PropertyAssignment`
        """

    @object_dict_field(AttributeAssignment)
    def attributes(self):
        """
        An optional list of attribute value assignments for the Node Template.
        
        :class:`AttributeAssignment`
        """

    @object_dict_field(RequirementAssignment)
    def requirements(self):
        """
        An optional sequenced list of requirement assignments for the Node Template.
        
        :class:`RequirementAssignment`
        """

    @object_dict_field(CapabilityAssignment)
    def capabilities(self):
        """
        An optional list of capability assignments for the Node Template.
        
        :class:`CapabilityAssignment`
        """

    @object_dict_field(InterfaceDefinition)
    def interfaces(self):
        """
        An optional list of named interface definitions for the Node Template.
        
        :class:`InterfaceDefinition`
        """

    @object_dict_field(ArtifactDefinition)
    def artifacts(self):
        """
        An optional list of named artifact definitions for the Node Template.
        
        :class:`ArtifactDefinition`
        """

    @object_dict_field(NodeFilter)
    def node_filter(self):
        """
        The optional filter definition that TOSCA orchestrators would use to select the correct target node. This keyname is only valid if the directive has the value of "selectable" set.
        
        :class:`NodeFilter`
        """

    @field_type(str)
    @primitive_field
    def copy(self):
        """
        The optional (symbolic) name of another node template to copy into (all keynames and values) and use as a basis for this node template.
        """

@has_fields
class RelationshipTemplate(Presentation):
    """
    A Relationship Template specifies the occurrence of a manageable relationship between node templates as part of an application's topology model that is defined in a TOSCA Service Template. A Relationship template is an instance of a specified Relationship Type and can provide customized properties, constraints or operations which override the defaults provided by its Relationship Type and its implementations.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_RELATIONSHIP_TEMPLATE>`__
    """

    @required_field
    @field_type(str)
    @primitive_field
    def type(self):
        """
        The required name of the Relationship Type the Relationship Template is based upon.
        """

    @field_type(str)
    @primitive_field
    def description(self):
        """
        An optional description for the Relationship Template.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @object_dict_field(PropertyAssignment)
    def properties(self):
        """
        An optional list of property assignments for the Relationship Template.
        
        :class:`PropertyAssignment`
        """

    @object_dict_field(AttributeAssignment)
    def attributes(self):
        """
        An optional list of attribute assignments for the Relationship Template.
        
        :class:`AttributeAssignment`
        """

    @object_dict_field(InterfaceDefinition)
    def interfaces(self):
        """
        An optional list of named interface definitions for the Node Template.
        
        :class:`InterfaceDefinition`
        """

    @field_type(str)
    @primitive_field
    def copy(self):
        """
        The optional (symbolic) name of another relationship template to copy into (all keynames and values) and use as a basis for this relationship template.
        """

@has_fields
class TopologyTemplate(Presentation):
    """
    This section defines the topology template of a cloud application. The main ingredients of the topology template are node templates representing components of the application and relationship templates representing links between the components. These elements are defined in the nested node_templates section and the nested relationship_templates sections, respectively. Furthermore, a topology template allows for defining input parameters, output parameters as well as grouping of node templates.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_TOPOLOGY_TEMPLATE>`__
    """

    @field_type(str)
    @primitive_field
    def description(self):
        """
        The optional description for the Topology Template.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        """

    @object_dict_field(ParameterDefinition)
    def inputs(self):
        """
        An optional list of input parameters (i.e., as parameter definitions) for the Topology Template.
        
        :class:`ParameterDefinition`
        """

    @object_dict_field(NodeTemplate)
    def node_templates(self):
        """
        An optional list of node template definitions for the Topology Template.
        
        :class:`NodeTemplate`
        """

    @object_dict_field(RelationshipTemplate)
    def relationship_templates(self):
        """
        An optional list of relationship templates for the Topology Template.
        
        :class:`RelationshipTemplate`
        """

    @object_dict_field(GroupDefinition)
    def groups(self):
        """
        An optional list of Group definitions whose members are node templates defined within this same Topology Template.
        
        :class:`GroupDefinition`
        """

    @object_dict_field(PolicyDefinition)
    def policies(self):
        """
        An optional list of Policy definitions for the Topology Template.
        
        :class:`PolicyDefinition`
        """

    @object_dict_field(ParameterDefinition)
    def outputs(self):
        """
        An optional list of output parameters (i.e., as parameter definitions) for the Topology Template.
        
        :class:`ParameterDefinition`
        """
    
    @primitive_field
    def substitution_mappings(self):
        """
        An optional declaration that exports the topology template as an implementation of a Node type.

        This also includes the mappings between the external Node Types named capabilities and requirements to existing implementations of those capabilities and requirements on Node templates declared within the topology template.
        """
