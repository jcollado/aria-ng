
import aria.grammar

class ToscaSimpleGrammar1_0(aria.grammar.Grammar):
    """
    ARIA grammar for `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html>`.
    """
    
    @property
    def profile(self):
        return Profile(self.structure)

    def get_import_locators(self):
        return [i.file for i in self.profile.imports]

class Base(object):
    def __init__(self, structure={}):
        self.structure = structure

    def _get_primitive(self, name, default=None):
        return self.structure.get(name, default)

    def _get_primitive_list(self, name):
        return self.structure.get(name) or []

    def _get_object(self, name, cls):
        structure = self.structure.get(name)
        return cls(structure) if structure else None

    def _get_object_list(self, name, cls):
        structures = self.structure.get(name)
        return [cls(structure) for structure in structures] if structures else []

    def _get_object_dict(self, name, cls):
        structures = self.structure.get(name)
        return {name: cls(structure) for name, structure in structures.iteritems()} if structures else {}

class Profile(Base):
    """
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc445238241>`.
    """

    @property
    def tosca_definitions_version(self):
        """
        This required element provides a means to include a reference to the TOSCA Simple Profile specification within the TOSCA Definitions YAML file.  It is an indicator for the version of the TOSCA grammar that should be used to parse the remainder of the document.
        
        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc379455047>`
        """
        return self._get_primitive('tosca_definitions_version')
        
    @tosca_definitions_version.setter
    def tosca_definitions_version(self, value):
        self.structure['tosca_definitions_version'] = value

    @property
    def metadata(self):
        """
        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc379455048>`
        """
        return self.structure.get('metadata')

    @property
    def description(self):
        """
        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`
        """
        return self._get_primitive('description')
    
    @description.setter
    def description(self, value):
        self.structure['description'] = value
        
    @property
    def dsl_definitions(self):
        # TODO ???
        return self.structure.get('dsl_definitions')
        
    @property
    def repositories(self):
        """
        :class:`Repository`
        """
        return self._get_object_list('repositories', Repository)

    @property
    def imports(self):
        """
        :class:`Import`
        """
        return self._get_object_list('imports', Import)
        
    @property
    def artifact_types(self):
        """
        :class:`ArtifactType`
        """
        return self._get_object_list('artifacts', ArtifactType)
        
    @property
    def data_types(self):
        """
        :class:`DataType`
        """
        return self._get_object_list('data_types', DataType)
        
    @property
    def capability_types(self):
        """
        :class:`CapabilityType`
        """
        return self._get_object_list('capability_types', CapabilityType)
        
    @property
    def interface_types(self):
        """
        :class:`InterfaceType`
        """
        return self._get_object_list('interface_types', InterfaceType)
        
    @property
    def relationship_types(self):
        """
        :class:`RelationshipType`
        """
        return self._get_object_list('relationship_types', RelationshipType)

    @property
    def node_types(self):
        """
        :class:`NodeType`
        """
        return self._get_object_list('node_types', NodeType)

    @property
    def group_types(self):
        """
        :class:`GroupType`
        """
        return self._get_object_list('group_types', GroupType)

    @property
    def policy_types(self):
        """
        :class:`PolicyType`
        """
        return self._get_object_list('policy_types', PolicyType)

    @property
    def topology_template(self):
        """
        :class:`TopologyTemplate`
        """
        return self._get_object('topology_template', TopologyTemplate)

class Repository(Base):
    """
    A repository definition defines a named external repository which contains deployment and implementation artifacts that are referenced within the TOSCA Service Template.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_REPOSITORY_DEF>`
    """
    
    DESCRIPTION = 'A repository definition defines a named external repository which contains deployment and implementation artifacts that are referenced within the TOSCA Service Template.'
    
    REQUIRED = ['url']
    
    @property
    def description(self):
        """
        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`
        """
        return self._get_primitive('description')

    @property
    def url(self):
        return self._get_primitive('url')

    @property
    def credential(self):
        """
        :class:`tosca.datatypes.Credential`
        """
        return self._get_object('credential', tosca.datatypes.Credential)

class Import(Base):
    """
    An import definition is used within a TOSCA Service Template to locate and uniquely name another TOSCA Service Template file which has type and template definitions to be imported (included) and referenced within another Service Template.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_IMPORT_DEF>`
    """
    
    DESCRIPTION = 'An import definition is used within a TOSCA Service Template to locate and uniquely name another TOSCA Service Template file which has type and template definitions to be imported (included) and referenced within another Service Template.'
    
    REQUIRED = ['file']

    def __init__(self, structure={}):
        super(Import, self).__init__({'file': structure} if isinstance(structure, basestring) else structure)

    @property
    def file(self):
        return self._get_primitive('file')

    @file.setter
    def file(self, value):
        self.structure['file'] = value

    @property
    def repository(self):
        return self._get_primitive('repository')

    @repository.setter
    def repository(self, value):
        self.structure['repository'] = value

    @property
    def namespace_uri(self):
        return self._get_primitive('namespace_uri')

    @namespace_uri.setter
    def namespace_uri(self, value):
        self.structure['namespace_uri'] = value

    @property
    def namespace_prefix(self):
        return self._get_primitive('namespace_prefix')

    @namespace_prefix.setter
    def namespace_prefix(self, value):
        self.structure['namespace_prefix'] = value

class ArtifactType(Base):
    """
    An Artifact Type is a reusable entity that defines the type of one or more files that are used to define implementation or deployment artifacts that are referenced by nodes or relationships on their operations.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_ARTIFACT_TYPE>`
    """
    
    DESCRIPTION = 'An Artifact Type is a reusable entity that defines the type of one or more files that are used to define implementation or deployment artifacts that are referenced by nodes or relationships on their operations.'

    @property
    def derived_from(self):
        return self._get_primitive('derived_from')

    @property
    def version(self):
        """
        :class:`Version'
        """
        return self._get_object('version', Version)

    @property
    def description(self):
        """
        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`
        """
        return self._get_primitive('description')

    @property
    def mime_type(self):
        return self._get_primitive('mime_type')

    @property
    def file_ext(self):
        return self._get_primitive_list('file_ext')

    @property
    def properties(self):
        """
        :class:`PropertyDefinition`
        """
        return self._get_object_list('properties', PropertyDefinition)

class DataType(Base):
    """
    A Data Type definition defines the schema for new named datatypes in TOSCA.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_DATA_TYPE>`
    """
    
    DESCRIPTION = 'A Data Type definition defines the schema for new named datatypes in TOSCA.'

    @property
    def derived_from(self):
        return self._get_primitive('derived_from')

    @property
    def version(self):
        """
        :class:`Version'
        """
        return self._get_object('version', Version)

    @property
    def description(self):
        """
        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`
        """
        return self._get_primitive('description')

    @property
    def constraints(self):
        """
        :class:`ConstraintClause`
        """
        return self._get_object_list('constraints', ConstraintClause)

    @property
    def properties(self):
        """
        :class:`PropertyDefinition`
        """
        return self._get_object_list('properties', PropertyDefinition)

class CapabilityType(Base):
    """
    A Capability Type is a reusable entity that describes a kind of capability that a Node Type can declare to expose. Requirements (implicit or explicit) that are declared as part of one node can be matched to (i.e., fulfilled by) the Capabilities declared by another node.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_CAPABILITY_TYPE>`
    """
    
    DESCRIPTION = 'A Capability Type is a reusable entity that describes a kind of capability that a Node Type can declare to expose. Requirements (implicit or explicit) that are declared as part of one node can be matched to (i.e., fulfilled by) the Capabilities declared by another node.'

    @property
    def derived_from(self):
        return self._get_primitive('derived_from')

    @property
    def version(self):
        """
        :class:`Version'
        """
        return self._get_object('version', Version)

    @property
    def description(self):
        """
        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`
        """
        return self._get_primitive('description')

    @property
    def properties(self):
        """
        :class:`PropertyDefinition`
        """
        return self._get_object_list('properties', PropertyDefinition)

    @property
    def attributes(self):
        """
        :class:`AttributeDefinition`
        """
        return self._get_object_list('attributes', AttributeDefinition)

    @property
    def valid_source_types(self):
        return self._get_primitive_list('valid_source_types')

class InterfaceType(Base):
    """
    An Interface Type is a reusable entity that describes a set of operations that can be used to interact with or manage a node or relationship in a TOSCA topology.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_INTERFACE_TYPE>`
    """
    
    DESCRIPTION = 'An Interface Type is a reusable entity that describes a set of operations that can be used to interact with or manage a node or relationship in a TOSCA topology.'

    @property
    def derived_from(self):
        return self._get_primitive('derived_from')

    @property
    def version(self):
        """
        :class:`Version'
        """
        return self._get_object('version', Version)

    @property
    def description(self):
        """
        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`
        """
        return self._get_primitive('description')

    @property
    def inputs(self):
        """
        :class:`PropertyDefinition`
        """
        return self._get_object_list('inputs', PropertyDefinition)

class RelationshipType(Base):
    """
    A Relationship Type is a reusable entity that defines the type of one or more relationships between Node Types or Node Templates.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_RELATIONSHIP_TYPE>`
    """
    
    DESCRIPTION = 'A Relationship Type is a reusable entity that defines the type of one or more relationships between Node Types or Node Templates.'

    @property
    def derived_from(self):
        return self._get_primitive('derived_from')

    @property
    def version(self):
        """
        :class:`Version'
        """
        return self._get_object('version', Version)

    @property
    def description(self):
        """
        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`
        """
        return self._get_primitive('description')

    @property
    def properties(self):
        """
        :class:`PropertyDefinition`
        """
        return self._get_object_list('properties', PropertyDefinition)

    @property
    def attributes(self):
        """
        :class:`AttributeDefinition`
        """
        return self._get_object_list('attributes', AttributeDefinition)

    @property
    def interfaces(self):
        """
        :class:`InterfaceDefinition`
        """
        return self._get_object_list('interfaces', InterfaceDefinition)

    @property
    def valid_target_types(self):
        return self._get_primitive_list('valid_target_types')

class NodeType(Base):
    """
    A Node Type is a reusable entity that defines the type of one or more Node Templates. As such, a Node Type defines the structure of observable properties via a Properties Definition, the Requirements and Capabilities of the node as well as its supported interfaces.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_NODE_TYPE>`
    """
    
    DESCRIPTION = 'A Node Type is a reusable entity that defines the type of one or more Node Templates. As such, a Node Type defines the structure of observable properties via a Properties Definition, the Requirements and Capabilities of the node as well as its supported interfaces.'

    @property
    def derived_from(self):
        return self._get_primitive('derived_from')

    @property
    def version(self):
        """
        :class:`Version'
        """
        return self._get_object('version', Version)

    @property
    def description(self):
        """
        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`
        """
        return self._get_primitive('description')

    @property
    def properties(self):
        """
        :class:`PropertyDefinition`
        """
        return self._get_object_list('properties', PropertyDefinition)

    @property
    def attributes(self):
        """
        :class:`AttributeDefinition`
        """
        return self._get_object_list('attributes', AttributeDefinition)

    @property
    def requirements(self):
        """
        :class:`RequirementDefinition`
        """
        return self._get_object_list('requirements', RequirementDefinition)

    @property
    def capabilities(self):
        """
        :class:`CapabilityDefinition`
        """
        return self._get_object_list('capabilities', CapabilityDefinition)

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

class GroupType(Base):
    """
    A Group Type defines logical grouping types for nodes, typically for different management purposes. Groups can effectively be viewed as logical nodes that are not part of the physical deployment topology of an application, yet can have capabilities and the ability to attach policies and interfaces that can be applied (depending on the group type) to its member nodes.

    Conceptually, group definitions allow the creation of logical "membership" relationships to nodes in a service template that are not a part of the application's explicit requirement dependencies in the topology template (i.e. those required to actually get the application deployed and running). Instead, such logical membership allows for the introduction of things such as group management and uniform application of policies (i.e., requirements that are also not bound to the application itself) to the group's members.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_GROUP_TYPE>`
    """
    
    DESCRIPTION = 'A Group Type defines logical grouping types for nodes, typically for different management purposes. Groups can effectively be viewed as logical nodes that are not part of the physical deployment topology of an application, yet can have capabilities and the ability to attach policies and interfaces that can be applied (depending on the group type) to its member nodes.'

    @property
    def derived_from(self):
        return self._get_primitive('derived_from')

    @property
    def version(self):
        """
        :class:`Version'
        """
        return self._get_object('version', Version)

    @property
    def description(self):
        """
        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`
        """
        return self._get_primitive('description')

    @property
    def properties(self):
        """
        :class:`PropertyDefinition`
        """
        return self._get_object_list('properties', PropertyDefinition)

    @property
    def members(self):
        return self._get_primitive_list('members')

    @property
    def interfaces(self):
        """
        :class:`InterfaceDefinition`
        """
        return self._get_object_list('interfaces', InterfaceDefinition)

class PolicyType(Base):
    """
    A Policy Type defines a type of requirement that affects or governs an application or service's topology at some stage of its lifecycle, but is not explicitly part of the topology itself (i.e., it does not prevent the application or service from being deployed or run if it did not exist).
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_POLICY_TYPE>`
    """
    
    DESCRIPTION = 'A Policy Type defines a type of requirement that affects or governs an application or service\'s topology at some stage of its lifecycle, but is not explicitly part of the topology itself (i.e., it does not prevent the application or service from being deployed or run if it did not exist).'

    @property
    def derived_from(self):
        return self._get_primitive('derived_from')

    @property
    def version(self):
        """
        :class:`Version'
        """
        return self._get_object('version', Version)

    @property
    def description(self):
        """
        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`
        """
        return self._get_primitive('description')

    @property
    def properties(self):
        """
        :class:`PropertyDefinition`
        """
        return self._get_object_list('properties', PropertyDefinition)

    @property
    def targets(self):
        return self._get_primitive_list('targets')

class TopologyTemplate(Base):
    """
    This section defines the topology template of a cloud application. The main ingredients of the topology template are node templates representing components of the application and relationship templates representing links between the components. These elements are defined in the nested node_templates section and the nested relationship_templates sections, respectively. Furthermore, a topology template allows for defining input parameters, output parameters as well as grouping of node templates.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_TOPOLOGY_TEMPLATE>`
    """
    
    DESCRIPTION = 'This section defines the topology template of a cloud application. The main ingredients of the topology template are node templates representing components of the application and relationship templates representing links between the components. These elements are defined in the nested node_templates section and the nested relationship_templates sections, respectively. Furthermore, a topology template allows for defining input parameters, output parameters as well as grouping of node templates.'

    @property
    def description(self):
        """
        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`
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

class PropertyDefinition(Base):
    """
    A property definition defines a named, typed value and related data that can be associated with an entity defined in this specification (e.g., Node Types, Relationship Types, Capability Types, etc.). Properties are used by template authors to provide input values to TOSCA entities which indicate their "desired state" when they are instantiated. The value of a property can be retrieved using the get_property function within TOSCA Service Templates.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_PROPERTY_DEFN>`
    """
    
    DESCRIPTION = 'A property definition defines a named, typed value and related data that can be associated with an entity defined in this specification (e.g., Node Types, Relationship Types, Capability Types, etc.). Properties are used by template authors to provide input values to TOSCA entities which indicate their "desired state" when they are instantiated. The value of a property can be retrieved using the get_property function within TOSCA Service Templates.'
    
    REQUIRED = ['type']
    
    @property
    def type(self):
        return self._get_primitive('type')
    
    @property
    def description(self):
        """
        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`
        """
        return self._get_primitive('description')

    @property
    def required(self):
        return self._get_primitive('required', True)

    @property
    def default(self):
        return self._get_primitive('default')

    @property
    def status(self):
        return self._get_primitive('status', 'supported')

    @property
    def constraints(self):
        """
        :class:`ConstraintClause`
        """
        return self._get_object_list('constraints', ConstraintClause)

    @property
    def entry_schema(self):
        return self._get_primitive('entry_schema')

class PropertyAssignment(Base):
    """
    This section defines the grammar for assigning values to named properties within TOSCA Node and Relationship templates that are defined in their corresponding named types.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_PROPERTY_VALUE_ASSIGNMENT>`
    """
    
    DESCRIPTION = 'This section defines the grammar for assigning values to named properties within TOSCA Node and Relationship templates that are defined in their corresponding named types.'
    
    # TODO

class ConstraintClause(Base):
    """
    A constraint clause defines an operation along with one or more compatible values that can be used to define a constraint on a property or parameter's allowed values when it is defined in a TOSCA Service Template or one of its entities.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_CONSTRAINTS_CLAUSE>`
    """
    
    DESCRIPTION = 'A constraint clause defines an operation along with one or more compatible values that can be used to define a constraint on a property or parameter\'s allowed values when it is defined in a TOSCA Service Template or one of its entities.'
    
    @property
    def equal(self):
        return self._get_primitive('equal')
    
    @property
    def greater_than(self):
        return self._get_primitive('greater_than')
    
    @property
    def greater_or_equal(self):
        return self._get_primitive('greater_or_equal')
    
    @property
    def less_than(self):
        return self._get_primitive('less_than')
    
    @property
    def less_or_equal(self):
        return self._get_primitive('less_or_equal')
    
    @property
    def in_range(self):
        return self._get_object('in_range', Range)
    
    @property
    def valid_values(self):
        return self._get_primitive_list('valid_values')
    
    @property
    def length(self):
        return self._get_primitive('length')
    
    @property
    def min_length(self):
        return self._get_primitive('min_length')
    
    @property
    def max_length(self):
        return self._get_primitive('max_length')

    @property
    def pattern(self):
        return self._get_primitive('pattern')

class AttributeDefinition(Base):
    """
    An attribute definition defines a named, typed value that can be associated with an entity defined in this specification (e.g., a Node, Relationship or Capability Type). Specifically, it is used to expose the "actual state" of some property of a TOSCA entity after it has been deployed and instantiated (as set by the TOSCA orchestrator). Attribute values can be retrieved via the get_attribute function from the instance model and used as values to other entities within TOSCA Service Templates.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_ATTRIBUTE_DEFN>`
    """
    
    DESCRIPTION = 'An attribute definition defines a named, typed value that can be associated with an entity defined in this specification (e.g., a Node, Relationship or Capability Type). Specifically, it is used to expose the "actual state" of some property of a TOSCA entity after it has been deployed and instantiated (as set by the TOSCA orchestrator). Attribute values can be retrieved via the get_attribute function from the instance model and used as values to other entities within TOSCA Service Templates.'
    
    REQUIRED = ['type']

    @property
    def type(self):
        return self._get_primitive('type')
    
    @property
    def description(self):
        """
        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`
        """
        return self._get_primitive('description')

    @property
    def default(self):
        return self._get_primitive('default')

    @property
    def status(self):
        return self._get_primitive('status', 'supported')

    @property
    def entry_schema(self):
        return self._get_primitive('entry_schema')

class InterfaceDefinition(Base):
    """
    An interface definition defines a named interface that can be associated with a Node or Relationship Type.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_INTERFACE_DEF>`
    """
    
    DESCRIPTION = 'An interface definition defines a named interface that can be associated with a Node or Relationship Type.'

    @property
    def inputs(self):
        """
        :class:`ParameterDefinition`
        """
        return self._get_object_list('inputs', ParameterDefinition)

    @property
    def properties(self):
        """
        :class:`PropertyDefinition` or :class:`PropertyAssignment'
        """
        # TODO
        return self._get_object_list('properties', PropertyDefinition)

class RequirementDefinition(Base):
    """
    The Requirement definition describes a named requirement (dependencies) of a TOSCA Node Type or Node template which needs to be fulfilled by a matching Capability definition declared by another TOSCA modelable entity. The requirement definition may itself include the specific name of the fulfilling entity (explicitly) or provide an abstract type, along with additional filtering characteristics, that a TOSCA orchestrator can use to fulfill the capability at runtime (implicitly).
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_REQUIREMENT_DEF>`
    """
    
    DESCRIPTION = 'The Requirement definition describes a named requirement (dependencies) of a TOSCA Node Type or Node template which needs to be fulfilled by a matching Capability definition declared by another TOSCA modelable entity. The requirement definition may itself include the specific name of the fulfilling entity (explicitly) or provide an abstract type, along with additional filtering characteristics, that a TOSCA orchestrator can use to fulfill the capability at runtime (implicitly).'
    
    REQUIRED = ['capability']

    @property
    def capability(self):
        return self._get_primitive('capability')

    @property
    def node(self):
        return self._get_primitive('node')

    @property
    def relationship(self):
        return self._get_primitive('relationship')

    @property
    def occurrences(self):
        # TODO: range of integer
        return self._get_object('occurrences', Range)

class RequirementAssignment(Base):
    """
    A Requirement assignment allows template authors to provide either concrete names of TOSCA templates or provide abstract selection criteria for providers to use to find matching TOSCA templates that are used to fulfill a named requirement's declared TOSCA Node Type.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_REQUIREMENT_ASSIGNMENT>`
    """
    
    DESCRIPTION = 'A Requirement assignment allows template authors to provide either concrete names of TOSCA templates or provide abstract selection criteria for providers to use to find matching TOSCA templates that are used to fulfill a named requirement\'s declared TOSCA Node Type.'
    
    #TODO

class CapabilityDefinition(Base):
    """
    A capability definition defines a named, typed set of data that can be associated with Node Type or Node Template to describe a transparent capability or feature of the software component the node describes.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_CAPABILITY_DEFN>`
    """
    
    DESCRIPTION = 'A capability definition defines a named, typed set of data that can be associated with Node Type or Node Template to describe a transparent capability or feature of the software component the node describes.'
    
    REQUIRED = ['type']

    @property
    def type(self):
        return self._get_primitive('type')
    
    @property
    def description(self):
        """
        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`
        """
        return self._get_primitive('description')

    @property
    def properties(self):
        """
        :class:`PropertyDefinition`
        """
        return self._get_object_list('properties', PropertyDefinition)

    @property
    def attributes(self):
        """
        :class:`AttributeDefinition`
        """
        return self._get_object_list('attributes', AttributeDefinition)

    @property
    def valid_source_types(self):
        return self._get_primitive_list('valid_source_types')

    @property
    def occurrences(self):
        # TODO: range of integer
        return self._get_object('occurrences', Range)

class CapabilityAssignment(Base):
    """
    A capability assignment allows node template authors to assign values to properties and attributes for a named capability definition that is part of a Node Template's type definition.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_CAPABILITY_ASSIGNMENT>`
    """
    
    DESCRIPTION = 'A capability assignment allows node template authors to assign values to properties and attributes for a named capability definition that is part of a Node Template\'s type definition.'
    
    #TODO

class ArtifactDefinition(Base):
    """
    An artifact definition defines a named, typed file that can be associated with Node Type or Node Template and used by orchestration engine to facilitate deployment and implementation of interface operations.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_ARTIFACT_DEF>`
    """
    
    DESCRIPTION = 'An artifact definition defines a named, typed file that can be associated with Node Type or Node Template and used by orchestration engine to facilitate deployment and implementation of interface operations.'
    
    REQUIRED = ['type', 'file']

    @property
    def type(self):
        return self._get_primitive('type')

    @property
    def file(self):
        return self._get_primitive('file')
    
    @property
    def repository(self):
        return self._get_primitive('repository')

    @property
    def description(self):
        """
        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`
        """
        return self._get_primitive('description')

    @property
    def deploy_path(self):
        return self._get_primitive('deploy_path')

class AttributeAssignment(Base):
    """
    This section defines the grammar for assigning values to named attributes within TOSCA Node and Relationship templates which are defined in their corresponding named types.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_ATTRIBUTE_VALUE_ASSIGNMENT>`
    """
    
    DESCRIPTION = 'This section defines the grammar for assigning values to named attributes within TOSCA Node and Relationship templates which are defined in their corresponding named types.'
    
    #TODO

class ParameterDefinition(Base):
    """
    A parameter definition is essentially a TOSCA property definition; however, it also allows a value to be assigned to it (as for a TOSCA property assignment). In addition, in the case of output parameters, it can optionally inherit the data type of the value assigned to it rather than have an explicit data type defined for it.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_PARAMETER_DEF>`
    """
    
    DESCRIPTION = 'A parameter definition is essentially a TOSCA property definition; however, it also allows a value to be assigned to it (as for a TOSCA property assignment). In addition, in the case of output parameters, it can optionally inherit the data type of the value assigned to it rather than have an explicit data type defined for it.'

    @property
    def type(self):
        return self._get_primitive('type')

    @property
    def value(self):
        return self._get_primitive('value')

class NodeTemplate(Base):
    """
    A Node Template specifies the occurrence of a manageable software component as part of an application's topology model which is defined in a TOSCA Service Template. A Node template is an instance of a specified Node Type and can provide customized properties, constraints or operations which override the defaults provided by its Node Type and its implementations.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_NODE_TEMPLATE>`
    """
    
    DESCRIPTION = 'A Node Template specifies the occurrence of a manageable software component as part of an application\'s topology model which is defined in a TOSCA Service Template. A Node template is an instance of a specified Node Type and can provide customized properties, constraints or operations which override the defaults provided by its Node Type and its implementations.'

    REQUIRED = ['type']

    @property
    def type(self):
        return self._get_primitive('type')

    @property
    def description(self):
        """
        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`
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
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_RELATIONSHIP_TEMPLATE>`
    """
    
    DESCRIPTION = 'A Relationship Template specifies the occurrence of a manageable relationship between node templates as part of an application\'s topology model that is defined in a TOSCA Service Template. A Relationship template is an instance of a specified Relationship Type and can provide customized properties, constraints or operations which override the defaults provided by its Relationship Type and its implementations.'

    REQUIRED = ['type']

    @property
    def type(self):
        return self._get_primitive('type')

    @property
    def description(self):
        """
        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`
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

class GroupDefinition(Base):
    """
    A group definition defines a logical grouping of node templates, typically for management purposes, but is separate from the application's topology template.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_GROUP_DEF>`
    """
    
    DESCRIPTION = 'A group definition defines a logical grouping of node templates, typically for management purposes, but is separate from the application\'s topology template.'

    REQUIRED = ['type']

    @property
    def type(self):
        return self._get_primitive('type')

    @property
    def description(self):
        """
        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`
        """
        return self._get_primitive('description')

    @property
    def properties(self):
        """
        :class:`PropertyAssignment`
        """
        return self._get_object_list('properties', PropertyAssignment)

    @property
    def members(self):
        return self._get_primitive_list('members')

    @property
    def interfaces(self):
        """
        :class:`InterfaceDefinition`
        """
        return self._get_object_list('interfaces', InterfaceDefinition)

class PolicyDefinition(Base):
    """
    A policy definition defines a policy that can be associated with a TOSCA topology or top-level entity definition (e.g., group definition, node template, etc.).
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_POLICY_DEF>`
    """
    
    DESCRIPTION = 'A policy definition defines a policy that can be associated with a TOSCA topology or top-level entity definition (e.g., group definition, node template, etc.).'

    REQUIRED = ['type']

    @property
    def type(self):
        return self._get_primitive('type')

    @property
    def description(self):
        """
        `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`
        """
        return self._get_primitive('description')

    @property
    def properties(self):
        """
        :class:`PropertyAssignment`
        """
        return self._get_object_list('properties', PropertyAssignment)

    @property
    def targets(self):
        return self._get_primitive_list('targets')

class NodeFilter(Base):
    """
    A node filter definition defines criteria for selection of a TOSCA Node Template based upon the template's property values, capabilities and capability properties.
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_NODE_FILTER_DEFN>`
    """
    
    DESCRIPTION = 'A node filter definition defines criteria for selection of a TOSCA Node Template based upon the template\'s property values, capabilities and capability properties.'

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
    
    `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_PROPERTY_FILTER_DEFN>`
    """
    
    DESCRIPTION = 'A property filter definition defines criteria, using constraint clauses, for selection of a TOSCA entity based upon it property values.'

    # TODO
