# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from urllib import pathname2url

from aria.reading.exceptions import ReaderNotFoundError

from .suite import (
    ParserTestCase,
    TempDirectoryTestCase,
    op_struct,
    parse_from_path,
    get_nodes_by_names,
)

AGENT = 'central_deployment_agent'
TYPE_HIERARCHY = 'type_hierarchy'
PLUGIN_EXECUTOR_KEY = 'executor'
PLUGIN_SOURCE_KEY = 'source'
PLUGIN_INSTALL_KEY = 'install'
PLUGIN_INSTALL_ARGUMENTS_KEY = 'install_arguments'
PLUGIN_NAME_KEY = 'name'
PLUGIN_PACKAGE_NAME = 'package_name'
PLUGIN_PACKAGE_VERSION = 'package_version'
PLUGIN_SUPPORTED_PLATFORM = 'supported_platform'
PLUGIN_DISTRIBUTION = 'distribution'
PLUGIN_DISTRIBUTION_VERSION = 'distribution_version'
PLUGIN_DISTRIBUTION_RELEASE = 'distribution_release'
NO_OP = {
    'implementation': '',
    'inputs': None,
    'executor': None,
    'max_retries': None,
    'retry_interval': None,
}


class _AssertionsMixin(object):
    """
    AssertionsMixin:
    give assert methods library for tests
    This mixin class requires TestCase base class
    """
    def assert_minimal_blueprint(self, result):
        self.assertEquals(1, len(result['nodes']))
        node = result['nodes'][0]
        self.assertEquals('test_node', node['id'])
        self.assertEquals('test_node', node['name'])
        self.assertEquals('test_type', node['type'])
        self.assertEquals('val', node['properties']['key'])

    def assert_blueprint(self, result):
        node = result['nodes'][0]
        operations = node['operations']
        for plugin in node['plugins']:
            if plugin['name'] == 'test_plugin':
                break
        else:
            self.fail('no plugin named test_plugin')

        self.assertEquals('test_type', node['type'])

        self.assertEquals(11, len(plugin))
        self.assertEquals('test_plugin', plugin[PLUGIN_NAME_KEY])

        self.assertEquals(
            op_struct('test_plugin', 'install', executor=AGENT),
            operations['install'])
        self.assertEquals(
            op_struct('test_plugin', 'install', executor=AGENT),
            operations['test_interface1.install'])
        self.assertEquals(
            op_struct('test_plugin', 'terminate', executor=AGENT),
            operations['terminate'])
        self.assertEquals(
            op_struct('test_plugin', 'terminate', executor=AGENT),
            operations['test_interface1.terminate'])


class TestParserApi(ParserTestCase, _AssertionsMixin):
    def test_minimal_blueprint(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_type_section()
        self.template.node_template_section()
        result = self.parse()
        self.assert_minimal_blueprint(result)

    def test_parse_dsl_from_bad_url(self):
        context = parse_from_path('http://www.google.com/bad-dsl')
        self.assertEqual(len(context.validation.issues), 1)
        issue = context.validation.issues[0]
        self.assertTrue(isinstance(issue.exception, ReaderNotFoundError))
        self.assertEqual(
            issue.exception.message,
            'location: http://www.google.com/bad-dsl')
        self.assertEqual(issue.level, 0)
        self.assertEqual(
            issue.message,
            'aria.reading.exceptions.ReaderNotFoundError was raised')

    # todo: move this tests to plugin tests?
    def test_type_with_single_explicit_interface_and_plugin(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_template_section()
        self.template.plugin_section()
        self.template += """
node_types:
  test_type:
    interfaces:
      test_interface1:
        install:
          implementation: test_plugin.install
          inputs: {}
        terminate:
          implementation: test_plugin.terminate
          inputs: {}
        start:
          implementation: test_plugin.start
          inputs: {}
    properties:
      install_agent:
        default: false
      key: {}
      number:
        default: 80
      boolean:
        default: false
      complex:
        default:
          key1: value1
          key2: value2
"""
        result = self.parse()
        self.assert_blueprint(result)

    def test_type_with_interfaces_and_basic_plugin(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_template_section()
        self.template.plugin_section()
        self.template += """
node_types:
  test_type:
    interfaces:
      test_interface1:
        install:
          implementation: test_plugin.install
          inputs: {}
        terminate:
          implementation: test_plugin.terminate
          inputs: {}
    properties:
      install_agent:
        default: 'false'
      key: {}
"""
        result = self.parse()
        self.assert_blueprint(result)
        first_node = result['nodes'][0]
        parsed_plugins = first_node['plugins']
        expected_plugins = [{
            PLUGIN_NAME_KEY: 'test_plugin',
            PLUGIN_SOURCE_KEY: 'dummy',
            PLUGIN_INSTALL_KEY: True,
            PLUGIN_EXECUTOR_KEY: AGENT,
            PLUGIN_INSTALL_ARGUMENTS_KEY: None,
            PLUGIN_PACKAGE_NAME: None,
            PLUGIN_PACKAGE_VERSION: None,
            PLUGIN_SUPPORTED_PLATFORM: None,
            PLUGIN_DISTRIBUTION: None,
            PLUGIN_DISTRIBUTION_VERSION: None,
            PLUGIN_DISTRIBUTION_RELEASE: None,
        }]
        self.assertEquals(parsed_plugins, expected_plugins)

    def test_type_with_interfaces_and_plugin_with_install_args(self):
        self.template.version_section('cloudify_dsl', '1.1')
        self.template.node_template_section()
        self.template += self.template.PLUGIN_WITH_INSTALL_ARGS
        self.template += self.template.BASIC_TYPE
        result = self.parse()
        self.assert_blueprint(result)
        first_node = result['nodes'][0]
        parsed_plugins = first_node['plugins']
        expected_plugins = [{
            PLUGIN_NAME_KEY: 'test_plugin',
            PLUGIN_SOURCE_KEY: 'dummy',
            PLUGIN_INSTALL_KEY: True,
            PLUGIN_EXECUTOR_KEY: AGENT,
            PLUGIN_INSTALL_ARGUMENTS_KEY: '-r requirements.txt',
            PLUGIN_PACKAGE_NAME: None,
            PLUGIN_PACKAGE_VERSION: None,
            PLUGIN_SUPPORTED_PLATFORM: None,
            PLUGIN_DISTRIBUTION: None,
            PLUGIN_DISTRIBUTION_VERSION: None,
            PLUGIN_DISTRIBUTION_RELEASE: None,
        }]
        self.assertEquals(parsed_plugins, expected_plugins)
    # todo: move this tests to plugin tests (end here)

    def test_import_empty_list(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_type_section()
        self.template.node_template_section()
        self.template += '\nimports: []\n'
        result = self.parse()
        self.assert_minimal_blueprint(result)

    def test_blueprint_description_field(self):
        self.template.node_type_section()
        self.template.node_template_section()
        self.template.version_section('cloudify_dsl', '1.2')
        self.template += '\ndescription: sample description\n'
        result = self.parse()
        self.assert_minimal_blueprint(result)
        self.assertIn('description', result)
        self.assertEquals('sample description', result['description'])

    def test_blueprint_description_field_omitted(self):
        self.template.node_type_section()
        self.template.node_template_section()
        self.template.version_section('cloudify_dsl', '1.2')
        result = self.parse()
        self.assert_minimal_blueprint(result)
        self.assertIn('description', result)
        self.assertEquals(None, result['description'])

    def test_node_get_type_properties_including_overriding_properties(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template += """
node_types:
  test_type:
    properties:
      key:
        default: not_val
      key2:
        default: val2
"""
        self.template.node_template_section()
        result = self.parse()
        # this will also check property "key" = "val"
        self.assert_minimal_blueprint(result)
        node = result['nodes'][0]
        self.assertEquals('val2', node['properties']['key2'])

    def test_type_properties_empty_properties(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template += """
node_types:
  test_type:
    properties: {}
node_templates:
  test_node:
    type: test_type
"""
        result = self.parse()
        self.assertEquals(1, len(result['nodes']))
        node = result['nodes'][0]
        self.assertEquals('test_node', node['id'])
        self.assertEquals('test_node', node['name'])
        self.assertEquals('test_type', node['type'])
        self.assertEqual(0, len(node['properties']))

    def test_type_properties_empty_property_override(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template += """
node_types:
  test_type:
    properties:
      key: {}
"""
        self.template.node_template_section()
        result = self.parse()
        self.assertEquals(1, len(result['nodes']))
        node = result['nodes'][0]
        self.assertEquals('test_node', node['id'])
        self.assertEquals('test_node', node['name'])
        self.assertEquals('test_type', node['type'])
        self.assertEquals('val', node['properties']['key'])
        # TODO: assert node-type's default and description values once
        # 'node_types' is part of the parser's output

    def test_type_properties_property_with_description_only(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template += """
node_types:
  test_type:
    properties:
      key:
        description: property_desc
"""
        self.template.node_template_section()
        result = self.parse()
        self.assertEquals(1, len(result['nodes']))
        node = result['nodes'][0]
        self.assertEquals('test_node', node['id'])
        self.assertEquals('test_node', node['name'])
        self.assertEquals('test_type', node['type'])
        self.assertEquals('val', node['properties']['key'])
        # TODO: assert type's default and description values once 'type' is
        # part of the parser's output

    def test_type_properties_standard_property(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template += """
node_types:
  test_type:
    properties:
      key:
        default: val
        description: property_desc
        type: string
"""
        self.template.node_template_section()
        result = self.parse()
        self.assertEquals(1, len(result['nodes']))
        node = result['nodes'][0]
        self.assertEquals('test_node', node['id'])
        self.assertEquals('test_node', node['name'])
        self.assertEquals('test_type', node['type'])
        self.assertEquals('val', node['properties']['key'])
        # TODO: assert type's default and description values once 'type' is
        # part of the parser's output

    def test_type_properties_derivation(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template += """
node_types:
  test_type:
    derived_from: test_type_parent
    properties:
      key:
        default: not_val
      key2:
        default: val2

  test_type_parent:
    properties:
      key:
        default: val1_parent
      key2:
        default: val2_parent
      key3:
        default: val3_parent
  """
        self.template.node_template_section()
        result = self.parse()
        # this will also check property "key" = "val"
        self.assert_minimal_blueprint(result)
        node = result['nodes'][0]
        self.assertEquals('val2', node['properties']['key2'])
        self.assertEquals('val3_parent', node['properties']['key3'])

    def test_empty_types_hierarchy_in_node(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_template_section()
        self.template += """
node_types:
  test_type:
    properties:
      key:
        default: not_val
      key2:
        default: val2
  """
        result = self.parse()
        node = result['nodes'][0]
        self.assertEqual(1, len(node[TYPE_HIERARCHY]))
        self.assertEqual('test_type', node[TYPE_HIERARCHY][0])

    def test_types_hierarchy_in_node(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_template_section()
        self.template += """
node_types:
  test_type:
    derived_from: test_type_parent
    properties:
      key:
        default: not_val
      key2:
        default: val2
  test_type_parent: {}
"""
        result = self.parse()
        node = result['nodes'][0]
        self.assertEqual(2, len(node[TYPE_HIERARCHY]))
        self.assertEqual('test_type_parent', node[TYPE_HIERARCHY][0])
        self.assertEqual('test_type', node[TYPE_HIERARCHY][1])

    def test_types_hierarchy_order_in_node(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_template_section()
        self.template += """
node_types:
  test_type:
    derived_from: test_type_parent
    properties:
      key:
        default: not_val
      key2:
        default: val2
  test_type_parent:
    derived_from: parent_type

  parent_type: {}
  """
        result = self.parse()
        node = result['nodes'][0]
        self.assertEqual(3, len(node[TYPE_HIERARCHY]))
        self.assertEqual('parent_type', node[TYPE_HIERARCHY][0])
        self.assertEqual('test_type_parent', node[TYPE_HIERARCHY][1])
        self.assertEqual('test_type', node[TYPE_HIERARCHY][2])

    def test_type_properties_recursive_derivation(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_template_section()
        self.template += """
node_types:
  test_type:
    derived_from: test_type_parent
    properties:
      key:
        default: not_val
      key2:
        default: val2

  test_type_parent:
    derived_from: test_type_grandparent
    properties:
      key:
        default: val_parent
      key2:
        default: val2_parent
      key4:
        default: val4_parent

  test_type_grandparent:
    derived_from: test_type_grandgrandparent
    properties:
      key:
        default: val1_grandparent
      key2:
        default: val2_grandparent
      key3:
        default: val3_grandparent

  test_type_grandgrandparent: {}
  """
        result = self.parse()
        self.assert_minimal_blueprint(result)
        node = result['nodes'][0]
        self.assertEquals('val2', node['properties']['key2'])
        self.assertEquals('val3_grandparent', node['properties']['key3'])
        self.assertEquals('val4_parent', node['properties']['key4'])

    def test_empty_top_level_relationships(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_type_section()
        self.template.node_template_section()
        self.template += """
relationships: {}
"""
        result = self.parse()
        self.assert_minimal_blueprint(result)
        self.assertEquals(0, len(result['relationships']))

    def test_empty_top_level_relationships_empty_relationship(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_type_section()
        self.template.node_template_section()
        self.template += """
relationships:
  test_relationship: {}
"""
        result = self.parse()
        self.assert_minimal_blueprint(result)
        self.assertEqual(
            {'name': 'test_relationship',
             'properties': {},
             'source_interfaces': {},
             'target_interfaces': {},
             'type_hierarchy': ['test_relationship']},
            result['relationships']['test_relationship'])

    def test_instance_relationships_empty_relationships_section(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_type_section()
        self.template.node_template_section()
        self.template += """
relationships: {}
"""
        result = self.parse()
        self.assert_minimal_blueprint(result)
        self.assertTrue(isinstance(result['nodes'][0]['relationships'], list))
        self.assertEqual(0, len(result['nodes'][0]['relationships']))

    def test_instance_relationships_standard_relationship(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_type_section()
        self.template.node_template_section()
        self.template += """
  test_node2:
    type: test_type
    relationships:
      -   type: test_relationship
          target: test_node
          source_interfaces:
            test_interface1:
              install: test_plugin.install
relationships:
  test_relationship: {}
plugins:
  test_plugin:
    executor: central_deployment_agent
    source: dummy
"""
        result = self.parse()
        self.assertEquals(2, len(result['nodes']))

        nodes = get_nodes_by_names(result, ['test_node', 'test_node2'])
        self.assertEquals('test_node2', nodes[0]['id'])
        self.assertEquals(1, len(nodes[0]['relationships']))

        relationship = nodes[0]['relationships'][0]
        self.assertEquals('test_relationship', relationship['type'])
        self.assertEquals('test_node', relationship['target_id'])
        self.assertEqual(
            {'implementation': 'test_plugin.install',
             'inputs': {},
             'executor': AGENT,
             'max_retries': None,
             'retry_interval': None},
            relationship['source_interfaces']['test_interface1']['install'])

        relationship_source_operations = relationship['source_operations']
        self.assertEqual(
            op_struct('test_plugin', 'install'),
            relationship_source_operations['install'])
        self.assertEqual(
            op_struct('test_plugin', 'install'),
            relationship_source_operations['test_interface1.install'])
        self.assertEqual(2, len(relationship_source_operations))
        self.assertEquals(8, len(relationship))

        plugin_def = nodes[0]['plugins'][0]
        self.assertEquals('test_plugin', plugin_def['name'])

    def test_instance_relationships_duplicate_relationship(self):
        # right now, having two relationships with the same (type,target)
        # under one node is valid
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_type_section()
        self.template.node_template_section()
        self.template += """
  test_node2:
    type: test_type
    relationships:
      -   type: test_relationship
          target: test_node
      -   type: test_relationship
          target: test_node
relationships:
  test_relationship: {}
"""
        result = self.parse()
        self.assertEquals(2, len(result['nodes']))

        node = get_nodes_by_names(result, ['test_node2'])[0]
        self.assertEquals('test_node2', node['id'])
        self.assertEquals(2, len(node['relationships']))
        self.assertEquals('test_relationship', node['relationships'][0]['type'])
        self.assertEquals('test_relationship', node['relationships'][1]['type'])
        self.assertEquals('test_node', node['relationships'][0]['target_id'])
        self.assertEquals('test_node', node['relationships'][1]['target_id'])
        self.assertEquals(8, len(node['relationships'][0]))
        self.assertEquals(8, len(node['relationships'][1]))

    def test_instance_relationships_relationship_inheritance(self):
        # possibly 'inheritance' is the wrong term to use here,
        # the meaning is for checking that the relationship properties from the
        # top-level relationships
        # section are used for instance-relationships which declare their types
        # note there are no overrides in this case; these are tested in the
        # next, more thorough test
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_type_section()
        self.template.node_template_section()
        self.template += """
  test_node2:
    type: test_type
    relationships:
      -   type: test_relationship
          target: test_node
          source_interfaces:
            interface1:
              op1: test_plugin.task_name1
relationships:
  relationship: {}
  test_relationship:
    derived_from: relationship
    target_interfaces:
      interface2:
        op2:
          implementation: test_plugin.task_name2
          inputs: {}
plugins:
  test_plugin:
    executor: central_deployment_agent
    source: dummy
"""
        result = self.parse()
        self.assertEquals(2, len(result['nodes']))

        nodes = get_nodes_by_names(result, ['test_node', 'test_node2'])
        relationship = nodes[0]['relationships'][0]
        self.assertEquals('test_relationship', relationship['type'])
        self.assertEquals('test_node', relationship['target_id'])
        self.assertEqual(
            {'implementation': 'test_plugin.task_name1',
             'inputs': {},
             'executor': AGENT,
             'max_retries': None,
             'retry_interval': None},
            relationship['source_interfaces']['interface1']['op1'])
        self.assertEqual(
            {'implementation': 'test_plugin.task_name2',
             'inputs': {},
             'executor': AGENT,
             'max_retries': None,
             'retry_interval': None},
            relationship['target_interfaces']['interface2']['op2'])

        rel_source_ops = relationship['source_operations']
        self.assertEqual(
            op_struct('test_plugin', 'task_name1', executor=AGENT),
            rel_source_ops['op1'])
        self.assertEqual(
            op_struct('test_plugin', 'task_name1', executor=AGENT),
            rel_source_ops['interface1.op1'])
        self.assertEquals(2, len(rel_source_ops))

        rel_target_ops = relationship['target_operations']
        self.assertEqual(
            op_struct('test_plugin', 'task_name2'),
            rel_target_ops['op2'])
        self.assertEqual(
            op_struct('test_plugin', 'task_name2'),
            rel_target_ops['interface2.op2'])
        self.assertEquals(2, len(rel_target_ops))
        self.assertEquals(8, len(relationship))

    def test_instance_relationship_properties_inheritance(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_type_section()
        self.template.node_template_section()
        self.template += """
  test_node2:
    type: test_type
    properties:
      key: "val"
    relationships:
      -   type: empty_relationship
          target: test_node
          properties:
            prop1: prop1_value_new
            prop2: prop2_value_new
            prop7: prop7_value_new_instance
relationships:
  empty_relationship:
    properties:
      prop1: {}
      prop2: {}
      prop7: {}
"""
        result = self.parse()
        self.assertEquals(2, len(result['nodes']))

        nodes = get_nodes_by_names(result, ['test_node', 'test_node2'])
        relationships = result['relationships']
        self.assertEquals(1, len(relationships))

        i_properties = nodes[0]['relationships'][0]['properties']
        self.assertEquals(3, len(i_properties))
        self.assertEquals('prop1_value_new', i_properties['prop1'])
        self.assertEquals('prop2_value_new', i_properties['prop2'])
        self.assertEquals('prop7_value_new_instance', i_properties['prop7'])

    def test_relationships_and_node_recursive_inheritance(self):
        # testing for a complete inheritance path for relationships
        # from top-level relationships to a relationship instance
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_type_section()
        self.template.node_template_section()
        self.template += """
  test_node2:
    type: test_type
    relationships:
      -   type: relationship
          target: test_node
          source_interfaces:
            test_interface3:
              install: test_plugin.install
          target_interfaces:
            test_interface1:
              install: test_plugin.install
relationships:
  relationship:
    derived_from: parent_relationship
    source_interfaces:
      test_interface2:
        install:
          implementation: test_plugin.install
          inputs: {}
        terminate:
          implementation: test_plugin.terminate
          inputs: {}
  parent_relationship:
    target_interfaces:
      test_interface3:
        install: {}
plugins:
  test_plugin:
    executor: central_deployment_agent
    source: dummy
"""
        result = self.parse()
        self.assertEquals(2, len(result['nodes']))

        nodes = get_nodes_by_names(result, ['test_node', 'test_node2'])
        node_relationship = nodes[0]['relationships'][0]
        relationship = result['relationships']['relationship']
        parent_relationship = result['relationships']['parent_relationship']
        self.assertEquals(2, len(result['relationships']))
        self.assertEquals(5, len(parent_relationship))
        self.assertEquals(6, len(relationship))
        self.assertEquals(8, len(node_relationship))
        self.assertEquals('parent_relationship', parent_relationship['name'])
        self.assertEquals(1, len(parent_relationship['target_interfaces']))
        self.assertEquals(
            1, len(parent_relationship['target_interfaces']['test_interface3']))
        self.assertEquals(
            {'implementation': '',
             'inputs': {},
             'executor': AGENT,
             'max_retries': None,
             'retry_interval': None},
            parent_relationship['target_interfaces']['test_interface3']['install'])

        self.assertEquals('relationship', relationship['name'])
        self.assertEquals('parent_relationship', relationship['derived_from'])
        self.assertEquals(1, len(relationship['target_interfaces']))
        self.assertEquals(
            1, len(relationship['target_interfaces']['test_interface3']))
        self.assertEquals(
            NO_OP, relationship['target_interfaces']['test_interface3']['install'])
        self.assertEquals(1, len(relationship['source_interfaces']))
        self.assertEquals(
            2, len(relationship['source_interfaces']['test_interface2']))
        self.assertEqual(
            {'implementation': 'test_plugin.install',
             'inputs': {},
             'executor': AGENT,
             'max_retries': None,
             'retry_interval': None},
            relationship['source_interfaces']['test_interface2']['install'])
        self.assertEqual(
            {'implementation': 'test_plugin.terminate',
             'inputs': {},
             'executor': AGENT,
             'max_retries': None,
             'retry_interval': None},
            relationship['source_interfaces']['test_interface2']['terminate'])
        self.assertEquals('relationship', node_relationship['type'])
        self.assertEquals('test_node', node_relationship['target_id'])
        self.assertEquals(2, len(node_relationship['target_interfaces']))
        self.assertEquals(
            1, len(node_relationship['target_interfaces']['test_interface3']))
        self.assertEquals(
            NO_OP, node_relationship['target_interfaces']['test_interface3']['install'])
        self.assertEquals(
            1, len(node_relationship['target_interfaces']['test_interface1']))

        self.assertEqual(
            {'implementation': 'test_plugin.install',
             'inputs': {},
             'executor': AGENT,
             'max_retries': None,
             'retry_interval': None},
            node_relationship['target_interfaces']['test_interface1']['install'])
        self.assertEquals(2, len(node_relationship['source_interfaces']))
        self.assertEquals(
            1, len(node_relationship['source_interfaces']['test_interface3']))
        self.assertEquals(
            {'implementation': 'test_plugin.install',
             'inputs': {},
             'executor': AGENT,
             'max_retries': None,
             'retry_interval': None},
            node_relationship['source_interfaces']['test_interface2']['install'])
        self.assertEquals(
            2, len(node_relationship['source_interfaces']['test_interface2']))
        self.assertEquals(
            {'implementation': 'test_plugin.install',
             'inputs': {},
             'executor': AGENT,
             'max_retries': None,
             'retry_interval': None},
            node_relationship['source_interfaces']['test_interface2']['install'])
        self.assertEquals(
            {'implementation': 'test_plugin.terminate',
             'inputs': {},
             'executor': AGENT,
             'max_retries': None,
             'retry_interval': None},
            node_relationship['source_interfaces']['test_interface2']['terminate'])

        rel_source_ops = node_relationship['source_operations']
        self.assertEquals(4, len(rel_source_ops))
        self.assertEqual(
            op_struct('test_plugin', 'install', executor=AGENT),
            rel_source_ops['test_interface2.install'])
        self.assertEqual(
            op_struct('test_plugin', 'install', executor=AGENT),
            rel_source_ops['test_interface3.install'])
        self.assertEqual(
            op_struct('test_plugin', 'terminate', executor=AGENT),
            rel_source_ops['terminate'])
        self.assertEqual(
            op_struct('test_plugin', 'terminate', executor=AGENT),
            rel_source_ops['test_interface2.terminate'])

        rel_target_ops = node_relationship['target_operations']
        self.assertEquals(2, len(rel_target_ops))
        self.assertEqual(
            op_struct('', '', {}, executor=AGENT),
            rel_target_ops['test_interface3.install'])
        self.assertEqual(
            op_struct('test_plugin', 'install', executor=AGENT),
            rel_target_ops['test_interface1.install'])

    def test_relationship_interfaces_inheritance_merge(self):
        # testing for a complete inheritance path for relationships
        # from top-level relationships to a relationship instance
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_type_section()
        self.template.node_template_section()
        self.template += """
  test_node2:
    type: test_type
    relationships:
      -   type: relationship
          target: test_node
          target_interfaces:
            test_interface:
              destroy: test_plugin.destroy1
          source_interfaces:
            test_interface:
              install2: test_plugin.install2
              destroy2: test_plugin.destroy2
relationships:
  parent_relationship:
    target_interfaces:
      test_interface:
        install: {}
    source_interfaces:
      test_interface:
        install2: {}
  relationship:
    derived_from: parent_relationship
    target_interfaces:
      test_interface:
        install:
          implementation: test_plugin.install
          inputs: {}
        terminate:
          implementation: test_plugin.terminate
          inputs: {}
    source_interfaces:
      test_interface:
        install2:
          implementation: test_plugin.install
          inputs: {}
        terminate2:
          implementation: test_plugin.terminate
          inputs: {}

plugins:
  test_plugin:
    executor: central_deployment_agent
    source: dummy
"""
        result = self.parse()
        self.assertEquals(2, len(result['nodes']))
        nodes = get_nodes_by_names(result, ['test_node', 'test_node2'])
        node_relationship = nodes[0]['relationships'][0]
        relationship = result['relationships']['relationship']
        parent_relationship = result['relationships']['parent_relationship']
        self.assertEquals(2, len(result['relationships']))
        self.assertEquals(5, len(parent_relationship))
        self.assertEquals(6, len(relationship))
        self.assertEquals(8, len(node_relationship))

        self.assertEquals('parent_relationship', parent_relationship['name'])
        self.assertEquals(1, len(parent_relationship['target_interfaces']))
        self.assertEquals(
            1, len(parent_relationship['target_interfaces']['test_interface']))
        self.assertIn(
            'install', parent_relationship['target_interfaces']['test_interface'])
        self.assertEquals(1, len(parent_relationship['source_interfaces']))
        self.assertEquals(
            1, len(parent_relationship['source_interfaces']['test_interface']))
        self.assertIn(
            'install2', parent_relationship['source_interfaces']['test_interface'])
        self.assertEquals('relationship', relationship['name'])
        self.assertEquals('parent_relationship', relationship['derived_from'])
        self.assertEquals(1, len(relationship['target_interfaces']))
        self.assertEquals(
            2, len(relationship['target_interfaces']['test_interface']))
        self.assertEqual(
            {'implementation': 'test_plugin.install',
             'inputs': {},
             'executor': AGENT,
             'max_retries': None,
             'retry_interval': None},
            relationship['target_interfaces']['test_interface']['install'])
        self.assertEqual(
            {'implementation': 'test_plugin.terminate',
             'inputs': {},
             'executor': AGENT,
             'max_retries': None,
             'retry_interval': None},
            relationship['target_interfaces']['test_interface']['terminate'])
        self.assertEquals(1, len(relationship['source_interfaces']))
        self.assertEquals(
            2, len(relationship['source_interfaces']['test_interface']))
        self.assertEqual(
            {'implementation': 'test_plugin.install',
             'inputs': {},
             'executor': AGENT,
             'max_retries': None,
             'retry_interval': None},
            relationship['source_interfaces']['test_interface']['install2'])
        self.assertEqual(
            {'implementation': 'test_plugin.terminate',
             'inputs': {},
             'executor': AGENT,
             'max_retries': None,
             'retry_interval': None},
            relationship['source_interfaces']['test_interface']['terminate2'])

        self.assertEquals('relationship', node_relationship['type'])
        self.assertEquals('test_node', node_relationship['target_id'])
        self.assertEquals(1, len(node_relationship['target_interfaces']))
        self.assertEquals(
            3, len(node_relationship['target_interfaces']['test_interface']))
        self.assertEqual(
            {'implementation': 'test_plugin.install',
             'inputs': {},
             'executor': AGENT,
             'max_retries': None,
             'retry_interval': None},
            node_relationship['target_interfaces']['test_interface']['install'])
        self.assertEqual(
            {'implementation': 'test_plugin.terminate',
             'inputs': {},
             'executor': AGENT,
             'max_retries': None,
             'retry_interval': None},
            relationship['target_interfaces']['test_interface']['terminate'])
        self.assertEqual(
            {'implementation': 'test_plugin.destroy1',
             'inputs': {},
             'executor': AGENT,
             'max_retries': None,
             'retry_interval': None},
            node_relationship['target_interfaces']['test_interface']['destroy'])
        self.assertEquals(1, len(node_relationship['source_interfaces']))
        self.assertEquals(
            3, len(node_relationship['source_interfaces']['test_interface']))
        self.assertEquals(
            {'implementation': 'test_plugin.install2',
             'inputs': {},
             'executor': AGENT,
             'max_retries': None,
             'retry_interval': None},
            node_relationship['source_interfaces']['test_interface']['install2'])
        self.assertEqual(
            {'implementation': 'test_plugin.terminate',
             'inputs': {},
             'executor': AGENT,
             'max_retries': None,
             'retry_interval': None},
            relationship['source_interfaces']['test_interface']['terminate2'])
        self.assertEquals(
            {'implementation': 'test_plugin.destroy2',
             'inputs': {},
             'executor': AGENT,
             'max_retries': None,
             'retry_interval': None},
            node_relationship['source_interfaces']['test_interface']['destroy2'])

        rel_source_ops = node_relationship['source_operations']
        self.assertEqual(
            op_struct('test_plugin', 'install2', executor=AGENT),
            rel_source_ops['install2'])
        self.assertEqual(
            op_struct('test_plugin', 'install2', executor=AGENT),
            rel_source_ops['test_interface.install2'])
        self.assertEqual(
            op_struct('test_plugin', 'terminate', executor=AGENT),
            rel_source_ops['terminate2'])
        self.assertEqual(
            op_struct('test_plugin', 'terminate', executor=AGENT),
            rel_source_ops['test_interface.terminate2'])
        self.assertEqual(
            op_struct('test_plugin', 'destroy2', executor=AGENT),
            rel_source_ops['destroy2'])
        self.assertEqual(
            op_struct('test_plugin', 'destroy2', executor=AGENT),
            rel_source_ops['test_interface.destroy2'])
        self.assertEquals(6, len(rel_source_ops))

        rel_target_ops = node_relationship['target_operations']
        self.assertEqual(
            op_struct('test_plugin', 'install', executor=AGENT),
            rel_target_ops['install'])
        self.assertEqual(
            op_struct('test_plugin', 'install', executor=AGENT),
            rel_target_ops['test_interface.install'])
        self.assertEqual(
            op_struct('test_plugin', 'terminate', executor=AGENT),
            rel_target_ops['terminate'])
        self.assertEqual(
            op_struct('test_plugin', 'terminate', executor=AGENT),
            rel_target_ops['test_interface.terminate'])
        self.assertEqual(
            op_struct('test_plugin', 'destroy1', executor=AGENT),
            rel_target_ops['destroy'])
        self.assertEqual(
            op_struct('test_plugin', 'destroy1', executor=AGENT),
            rel_target_ops['test_interface.destroy'])
        self.assertEquals(6, len(rel_source_ops))


class TestParserApiWithFileSystem(ParserTestCase, TempDirectoryTestCase, _AssertionsMixin):
    def test_import_from_path(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_type_section()
        self.template.node_template_section()
        template_as_import = self.create_yaml_with_imports([str(self.template)])
        self.template.clear()
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.template += template_as_import
        result = self.parse()
        self.assert_minimal_blueprint(result)

    def test_dsl_with_type_with_operation_mappings(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template += self.create_yaml_with_imports([
            self.template.BASIC_NODE_TEMPLATES_SECTION,
            self.template.BASIC_PLUGIN,
        ])
        self.template += """
node_types:
  test_type:
    properties:
      key: {}
    interfaces:
      test_interface1:
        install:
          implementation: test_plugin.install
          inputs: {}
        terminate:
          implementation: test_plugin.terminate
          inputs: {}
      test_interface2:
        start:
          implementation: other_test_plugin.start
          inputs: {}
        shutdown:
          implementation: other_test_plugin.shutdown
          inputs: {}

plugins:
  other_test_plugin:
    executor: central_deployment_agent
    source: dummy
"""
        result = self.parse()
        node = result['nodes'][0]
        operations = node['operations']

        self.assert_blueprint(result)
        self.assertEquals(
            op_struct('other_test_plugin', 'start', executor=AGENT),
            operations['start'])
        self.assertEquals(
            op_struct('other_test_plugin', 'start', executor=AGENT),
            operations['test_interface2.start'])
        self.assertEquals(
            op_struct('other_test_plugin', 'shutdown', executor=AGENT),
            operations['shutdown'])
        self.assertEquals(
            op_struct('other_test_plugin', 'shutdown', executor=AGENT),
            operations['test_interface2.shutdown'])

    def test_recursive_imports(self):
        template_to_import = (
            self.template.BASIC_PLUGIN
            + self.create_yaml_with_imports([self.template.BASIC_TYPE])
        )
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_template_section()
        self.template += self.create_yaml_with_imports([template_to_import])
        result = self.parse()
        self.assert_blueprint(result)

    def test_parse_dsl_from_file(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_type_section()
        self.template.node_template_section()
        filename = self.make_yaml_file(str(self.template))
        result = self.parse_from_uri(filename)
        self.assert_minimal_blueprint(result)

    def test_diamond_imports(self):

        bottom_file_content = self.template.BASIC_TYPE

        mid_file1_content = (
            self.create_yaml_with_imports([bottom_file_content])
            + self.template.BASIC_PLUGIN)
        mid_file2_content = self.create_yaml_with_imports([bottom_file_content])

        self.template.version_section('cloudify_dsl', '1.0')
        self.template += self.create_yaml_with_imports([
            mid_file1_content,
            mid_file2_content,
        ])
        self.template.node_template_section()

        result = self.parse()
        self.assert_blueprint(result)

    def test_type_interface_derivation(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template += self.create_yaml_with_imports([
            self.template.BASIC_NODE_TEMPLATES_SECTION,
            self.template.BASIC_PLUGIN,
        ])
        self.template += """
node_types:
  test_type:
    derived_from: test_type_parent
    properties:
      key: {}
    interfaces:
      test_interface1:
        install:
          implementation: test_plugin.install
          inputs: {}
        terminate:
          implementation: test_plugin.terminate
          inputs: {}
      test_interface2:
        start:
          implementation: test_plugin2.start
          inputs: {}
        stop:
          implementation: test_plugin2.stop
          inputs: {}
      test_interface3:
        op1:
          implementation: test_plugin3.op
          inputs: {}

  test_type_parent:
    interfaces:
      test_interface1:
        install:
          implementation: nop_plugin.install
          inputs: {}
        terminate:
          implementation: nop_plugin.install
          inputs: {}
      test_interface2:
        start:
          implementation: test_plugin2.start
          inputs: {}
        stop:
          implementation: test_plugin2.stop
          inputs: {}
      test_interface3:
        op1:
          implementation: test_plugin3.op
          inputs: {}
      test_interface4:
        op2:
          implementation: test_plugin4.op2
          inputs: {}

plugins:
  test_plugin2:
    executor: central_deployment_agent
    source: dummy
  test_plugin3:
    executor: central_deployment_agent
    source: dummy
  test_plugin4:
    executor: central_deployment_agent
    source: dummy
"""
        result = self.parse()
        self.assert_blueprint(result)

        node = result['nodes'][0]
        operations = node['operations']

        self.assertEquals(
            op_struct('test_plugin2', 'start', executor=AGENT),
            operations['start'])
        self.assertEquals(
            op_struct('test_plugin2', 'start', executor=AGENT),
            operations['test_interface2.start'])
        self.assertEquals(
            op_struct('test_plugin2', 'stop', executor=AGENT),
            operations['stop'])
        self.assertEquals(
            op_struct('test_plugin2', 'stop', executor=AGENT),
            operations['test_interface2.stop'])
        self.assertEquals(
            op_struct('test_plugin3', 'op', executor=AGENT),
            operations['op1'])
        self.assertEquals(
            op_struct('test_plugin3', 'op', executor=AGENT),
            operations['test_interface3.op1'])
        self.assertEquals(
            op_struct('test_plugin4', 'op2', executor=AGENT),
            operations['op2'])
        self.assertEquals(
            op_struct('test_plugin4', 'op2', executor=AGENT),
            operations['test_interface4.op2'])
        self.assertEquals(12, len(operations))
        self.assertEquals(4, len(node['plugins']))

    def test_type_interface_recursive_derivation(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template += self.create_yaml_with_imports([
            self.template.BASIC_NODE_TEMPLATES_SECTION,
            self.template.BASIC_PLUGIN])
        self.template += """
node_types:
  test_type:
    derived_from: test_type_parent
    properties:
      key: {}
    interfaces:
      test_interface1:
        install:
          implementation: test_plugin.install
          inputs: {}
        terminate:
          implementation: test_plugin.terminate
          inputs: {}

  test_type_parent:
    derived_from: test_type_grandparent

  test_type_grandparent:
    interfaces:
      test_interface1:
        install:
          implementation: non_plugin.install
          inputs: {}
        terminate:
          implementation: non_plugin.terminate
          inputs: {}
      test_interface2:
        start:
          implementation: test_plugin2.start
          inputs: {}
        stop:
          implementation: test_plugin2.stop
          inputs: {}

plugins:
  test_plugin2:
    executor: central_deployment_agent
    source: dummy
"""
        result = self.parse()
        self.assert_blueprint(result)
        node = result['nodes'][0]
        operations = node['operations']
        self.assertEquals(8, len(operations))
        self.assertEquals(
            op_struct('test_plugin2', 'start', executor=AGENT),
            operations['start'])
        self.assertEquals(
            op_struct('test_plugin2', 'start', executor=AGENT),
            operations['test_interface2.start'])
        self.assertEquals(
            op_struct('test_plugin2', 'stop', executor=AGENT),
            operations['stop'])
        self.assertEquals(
            op_struct('test_plugin2', 'stop', executor=AGENT),
            operations['test_interface2.stop'])
        self.assertEquals(2, len(node['plugins']))

    def test_two_explicit_interfaces_with_same_operation_name(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template += self.create_yaml_with_imports([
            self.template.BASIC_NODE_TEMPLATES_SECTION,
            self.template.BASIC_PLUGIN])
        self.template += """
node_types:
  test_type:
    properties:
      key: {}
    interfaces:
      test_interface1:
        install:
          implementation: test_plugin.install
          inputs: {}
        terminate:
          implementation: test_plugin.terminate
          inputs: {}
      test_interface2:
        install:
          implementation: other_test_plugin.install
          inputs: {}
        shutdown:
          implementation: other_test_plugin.shutdown
          inputs: {}
plugins:
  other_test_plugin:
    executor: central_deployment_agent
    source: dummy
"""
        result = self.parse()
        node = result['nodes'][0]
        self.assertEquals('test_type', node['type'])
        operations = node['operations']
        self.assertEquals(
            op_struct('test_plugin', 'install', executor=AGENT),
            operations['test_interface1.install'])
        self.assertEquals(
            op_struct('test_plugin', 'terminate', executor=AGENT),
            operations['test_interface1.terminate'])
        self.assertEquals(
            op_struct('other_test_plugin', 'install', executor=AGENT),
            operations['test_interface2.install'])
        self.assertEquals(
            op_struct('other_test_plugin', 'shutdown', executor=AGENT),
            operations['test_interface2.shutdown'])

        self.assertEquals(
            op_struct('test_plugin', 'terminate', executor=AGENT),
            operations['terminate'])
        self.assertEquals(
            op_struct('other_test_plugin', 'shutdown', executor=AGENT),
            operations['shutdown'])
        self.assertEquals(6, len(operations))

    def test_relative_path_import(self):
        self.write_to_file(self.template.BASIC_TYPE, 'bottom_level.yaml')

        mid_level_yaml = self.template.BASIC_PLUGIN + """
imports:
  -   \"bottom_level.yaml\""""
        mid_file_name = self.make_yaml_file(mid_level_yaml)

        top_level_yaml = self.template.BASIC_NODE_TEMPLATES_SECTION + """
imports:
  -   {0}""".format(mid_file_name)
        self.template.version_section('cloudify_dsl', '1.0')
        self.template += top_level_yaml
        result = self.parse(resources_base_url=self.temp_directory)
        self.assert_blueprint(result)

    def test_import_from_file_uri(self):
        self.template.node_type_section()
        self.template.node_template_section()
        data = self.create_yaml_with_imports([str(self.template)], True)
        self.template.clear()
        self.template.version_section('cloudify_dsl', '1.0')
        self.template += data
        result = self.parse()
        self.assert_minimal_blueprint(result)

    def test_relative_file_uri_import(self):
        self.write_to_file(self.template.BASIC_TYPE, 'bottom_level.yaml')

        mid_level_yaml = self.template.BASIC_PLUGIN + """
imports:
  -   \"bottom_level.yaml\"
"""
        mid_file_name = self.make_yaml_file(mid_level_yaml)

        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_template_section()
        self.template += """
imports:
  -   {0}""".format('file:///' + pathname2url(mid_file_name))

        result = self.parse(resources_base_url=self.temp_directory)
        self.assert_blueprint(result)
