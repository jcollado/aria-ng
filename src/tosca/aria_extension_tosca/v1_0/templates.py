
from .presentation import ToscaPresentation
from .misc import MetaData, Repository, Import
from .definitions import GroupDefinition, PolicyDefinition, ParameterDefinition, InterfaceDefinitionForTemplate, ArtifactDefinition
from .assignments import AttributeAssignment, RequirementAssignment, CapabilityAssignment
from .property_assignment import PropertyAssignment
from .types import ArtifactType, DataType, CapabilityType, InterfaceType, RelationshipType, NodeType, GroupType, PolicyType
from .filters import NodeFilter
from .utils.properties import get_assigned_and_defined_property_values
from .utils.interfaces import get_template_interfaces
from aria import dsl_specification
from aria.presentation import has_fields, primitive_field, primitive_list_field, object_field, object_list_field, object_dict_field, object_sequenced_list_field, field_validator, type_validator

@has_fields
@dsl_specification('3.7.3', 'tosca-simple-profile-1.0')
class NodeTemplate(ToscaPresentation):
    """
    A Node Template specifies the occurrence of a manageable software component as part of an application's topology model which is defined in a TOSCA Service Template. A Node template is an instance of a specified Node Type and can provide customized properties, constraints or operations which override the defaults provided by its Node Type and its implementations.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_NODE_TEMPLATE>`__
    """

    @field_validator(type_validator('node type', 'node_types'))
    @primitive_field(str, required=True)
    def type(self):
        """
        The required name of the Node Type the Node Template is based upon.
        
        :rtype: str
        """

    @primitive_field(str)
    def description(self):
        """
        An optional description for the Node Template.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

    @primitive_list_field(str)
    def directives(self):
        """
        An optional list of directive values to provide processing instructions to orchestrators and tooling.
        
        :rtype: list of str
        """

    @object_dict_field(PropertyAssignment)
    def properties(self):
        """
        An optional list of property value assignments for the Node Template.
        
        :rtype: dict of str, :class:`PropertyAssignment`
        """

    @object_dict_field(AttributeAssignment)
    def attributes(self):
        """
        An optional list of attribute value assignments for the Node Template.
        
        :rtype: dict of str, :class:`AttributeAssignment`
        """

    @object_sequenced_list_field(RequirementAssignment)
    def requirements(self):
        """
        An optional sequenced list of requirement assignments for the Node Template.
        
        :rtype: list of (str, :class:`RequirementAssignment`)
        """

    @object_dict_field(CapabilityAssignment)
    def capabilities(self):
        """
        An optional list of capability assignments for the Node Template.
        
        :rtype: dict of str, :class:`CapabilityAssignment`
        """

    @object_dict_field(InterfaceDefinitionForTemplate)
    def interfaces(self):
        """
        An optional list of named interface definitions for the Node Template.
        
        :rtype: dict of str, :class:`InterfaceDefinitionForTemplate`
        """

    @object_dict_field(ArtifactDefinition)
    def artifacts(self):
        """
        An optional list of named artifact definitions for the Node Template.
        
        :rtype: dict of str, :class:`ArtifactDefinition`
        """

    @object_dict_field(NodeFilter)
    def node_filter(self):
        """
        The optional filter definition that TOSCA orchestrators would use to select the correct target node. This keyname is only valid if the directive has the value of "selectable" set.
        
        :rtype: dict of str, :class:`NodeFilter`
        """

    @primitive_field(str)
    def copy(self):
        """
        The optional (symbolic) name of another node template to copy into (all keynames and values) and use as a basis for this node template.
        
        :rtype: str
        """
    
    def _get_type(self, context):
        return context.presentation.node_types.get(self.type)

    def _get_properties(self, context):
        return get_assigned_and_defined_property_values(context, self)

    def _get_interfaces(self, context):
        return get_template_interfaces(context, self, 'node template')

    def _validate(self, context):
        super(NodeTemplate, self)._validate(context)
        self._get_properties(context)
        self._get_interfaces(context)

@has_fields
@dsl_specification('3.7.4', 'tosca-simple-profile-1.0')
class RelationshipTemplate(ToscaPresentation):
    """
    A Relationship Template specifies the occurrence of a manageable relationship between node templates as part of an application's topology model that is defined in a TOSCA Service Template. A Relationship template is an instance of a specified Relationship Type and can provide customized properties, constraints or operations which override the defaults provided by its Relationship Type and its implementations.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_RELATIONSHIP_TEMPLATE>`__
    """

    @field_validator(type_validator('relationship type', 'relationship_types'))
    @primitive_field(str, required=True)
    def type(self):
        """
        The required name of the Relationship Type the Relationship Template is based upon.
        
        :rtype: str
        """

    @primitive_field(str)
    def description(self):
        """
        An optional description for the Relationship Template.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

    @object_dict_field(PropertyAssignment)
    def properties(self):
        """
        An optional list of property assignments for the Relationship Template.
        
        :rtype: dict of str, :class:`PropertyAssignment`
        """

    @object_dict_field(AttributeAssignment)
    def attributes(self):
        """
        An optional list of attribute assignments for the Relationship Template.
        
        :rtype: dict of str, :class:`AttributeAssignment`
        """

    @object_dict_field(InterfaceDefinitionForTemplate)
    def interfaces(self):
        """
        An optional list of named interface definitions for the Node Template.
        
        :rtype: dict of str, :class:`InterfaceDefinitionForTemplate`
        """

    @primitive_field(str)
    def copy(self):
        """
        The optional (symbolic) name of another relationship template to copy into (all keynames and values) and use as a basis for this relationship template.
        
        :rtype: str
        """

    def _get_type(self, context):
        return context.presentation.relationship_types.get(self.type)

    def _get_properties(self, context):
        return get_assigned_and_defined_property_values(context, self)

    def _get_interfaces(self, context):
        return get_template_interfaces(context, self, 'relationship template')
    
    def _validate(self, context):
        super(RelationshipTemplate, self)._validate(context)
        self._get_properties(context)
        self._get_interfaces(context)

@has_fields
@dsl_specification('3.8', 'tosca-simple-profile-1.0')
class TopologyTemplate(ToscaPresentation):
    """
    This section defines the topology template of a cloud application. The main ingredients of the topology template are node templates representing components of the application and relationship templates representing links between the components. These elements are defined in the nested node_templates section and the nested relationship_templates sections, respectively. Furthermore, a topology template allows for defining input parameters, output parameters as well as grouping of node templates.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_TOPOLOGY_TEMPLATE>`__
    """

    @primitive_field(str)
    def description(self):
        """
        The optional description for the Topology Template.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

    @object_dict_field(ParameterDefinition)
    def inputs(self):
        """
        An optional list of input parameters (i.e., as parameter definitions) for the Topology Template.
        
        :rtype: dict of str, :class:`ParameterDefinition`
        """

    @object_dict_field(NodeTemplate)
    def node_templates(self):
        """
        An optional list of node template definitions for the Topology Template.
        
        :rtype: dict of str, :class:`NodeTemplate`
        """

    @object_dict_field(RelationshipTemplate)
    def relationship_templates(self):
        """
        An optional list of relationship templates for the Topology Template.
        
        :rtype: dict of str, :class:`RelationshipTemplate`
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
        
        :rtype: dict of str, :class:`PolicyDefinition`
        """

    @object_dict_field(ParameterDefinition)
    def outputs(self):
        """
        An optional list of output parameters (i.e., as parameter definitions) for the Topology Template.
        
        :rtype: dict of str, :class:`ParameterDefinition`
        """
    
    @primitive_field()
    def substitution_mappings(self):
        """
        An optional declaration that exports the topology template as an implementation of a Node type.

        This also includes the mappings between the external Node Types named capabilities and requirements to existing implementations of those capabilities and requirements on Node templates declared within the topology template.
        """

@has_fields
@dsl_specification('3.9', 'tosca-simple-profile-1.0')
class ServiceTemplate(ToscaPresentation):
    """
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_SERVICE_TEMPLATE>`__.
    """
    
    @primitive_field(str)
    @dsl_specification('3.9.3.1', 'tosca-simple-profile-1.0')
    def tosca_definitions_version(self):
        """
        Defines the version of the TOSCA Simple Profile specification the template (grammar) complies with. 
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc379455047>`__
        
        See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-versioning/>`__
        
        :rtype: str
        """

    @object_field(MetaData)
    def metadata(self):
        """
        Defines a section used to declare additional metadata information. Domain-specific TOSCA profile specifications may define keynames that are required for their implementations.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc379455048>`__
        
        :rtype: :class:`MetaData`
        """

    @primitive_field(str)
    @dsl_specification('3.9.3.6', 'tosca-simple-profile-1.0')
    def description(self):
        """
        Declares a description for this Service Template and its contents.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """
    
    @primitive_field()
    @dsl_specification('3.9.3.7', 'tosca-simple-profile-1.0')
    def dsl_definitions(self):
        """
        Declares optional DSL-specific definitions and conventions. For example, in YAML, this allows defining reusable YAML macros (i.e., YAML alias anchors) for use throughout the TOSCA Service Template.

        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc397688790>`__
        """
        
    @object_dict_field(Repository)
    @dsl_specification('3.9.3.8', 'tosca-simple-profile-1.0')
    def repositories(self):
        """
        Declares the list of external repositories which contain artifacts that are referenced in the service template along with their addresses and necessary credential information used to connect to them in order to retrieve the artifacts.
        
        :rtype: dict of str, :class:`Repository`
        """

    @object_list_field(Import)
    @dsl_specification('3.9.3.9', 'tosca-simple-profile-1.0')
    def imports(self):
        """
        Declares import statements external TOSCA Definitions documents. For example, these may be file location or URIs relative to the service template file within the same TOSCA CSAR file.
        
        :rtype: list of :class:`Import`
        """
        
    @object_dict_field(ArtifactType)
    @dsl_specification('3.9.3.10', 'tosca-simple-profile-1.0')
    def artifact_types(self):
        """
        This section contains an optional list of artifact type definitions for use in the service template.
        
        :rtype: dict of str, :class:`ArtifactType`
        """
        
    @object_dict_field(DataType)
    @dsl_specification('3.9.3.11', 'tosca-simple-profile-1.0')
    def data_types(self):
        """
        Declares a list of optional TOSCA Data Type definitions.
        
        :rtype: dict of str, :class:`DataType`
        """
        
    @object_dict_field(CapabilityType)
    @dsl_specification('3.9.3.12', 'tosca-simple-profile-1.0')
    def capability_types(self):
        """
        This section contains an optional list of capability type definitions for use in the service template.
        
        :rtype: dict of str, :class:`CapabilityType`
        """
        
    @object_dict_field(InterfaceType)
    @dsl_specification('3.9.3.13', 'tosca-simple-profile-1.0')
    def interface_types(self):
        """
        This section contains an optional list of interface type definitions for use in the service template.
        
        :rtype: dict of str, :class:`InterfaceType`
        """
        
    @object_dict_field(RelationshipType)
    @dsl_specification('3.9.3.14', 'tosca-simple-profile-1.0')
    def relationship_types(self):
        """
        This section contains a set of relationship type definitions for use in the service template.
        
        :rtype: dict of str, :class:`RelationshipType`
        """

    @object_dict_field(NodeType)
    @dsl_specification('3.9.3.15', 'tosca-simple-profile-1.0')
    def node_types(self):
        """
        This section contains a set of node type definitions for use in the service template.
        
        :rtype: dict of str, :class:`NodeType`
        """

    @object_dict_field(GroupType)
    @dsl_specification('3.9.3.16', 'tosca-simple-profile-1.0')
    def group_types(self):
        """
        This section contains a list of group type definitions for use in the service template.
        
        :rtype: dict of str, :class:`GroupType`
        """

    @object_dict_field(PolicyType)
    @dsl_specification('3.9.3.17', 'tosca-simple-profile-1.0')
    def policy_types(self):
        """
        This section contains a list of policy type definitions for use in the service template.
        
        :rtype: dict of str, :class:`PolicyType`
        """

    @object_field(TopologyTemplate)
    def topology_template(self):
        """
        Defines the topology template of an application or service, consisting of node templates that represent the application's or service's components, as well as relationship templates representing relations between the components.
        
        :rtype: :class:`TopologyTemplate`
        """
