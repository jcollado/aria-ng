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

    def test_empty_types_hierarchy_in_node(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_template_section()
        self.template += """
node_types:
    test_type:
        properties:
            key:
                default: "not_val"
            key2:
                default: "val2"
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
        derived_from: "test_type_parent"
        properties:
            key:
                default: "not_val"
            key2:
                default: "val2"
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
        derived_from: "test_type_parent"
        properties:
            key:
                default: "not_val"
            key2:
                default: "val2"
    test_type_parent:
        derived_from: "parent_type"

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
        properties:
            key:
                default: "not_val"
            key2:
                default: "val2"
        derived_from: "test_type_parent"

    test_type_parent:
        properties:
            key:
                default: "val_parent"
            key2:
                default: "val2_parent"
            key4:
                default: "val4_parent"
        derived_from: "test_type_grandparent"

    test_type_grandparent:
        properties:
            key:
                default: "val1_grandparent"
            key2:
                default: "val2_grandparent"
            key3:
                default: "val3_grandparent"
        derived_from: "test_type_grandgrandparent"

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

    def test_type_interface_derivation(self):
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
                    implementation: test_plugin2.start
                    inputs: {}
                stop:
                    implementation: test_plugin2.stop
                    inputs: {}
            test_interface3:
                op1:
                    implementation: test_plugin3.op
                    inputs: {}
        derived_from: test_type_parent

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
        derived_from: test_type_parent

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
