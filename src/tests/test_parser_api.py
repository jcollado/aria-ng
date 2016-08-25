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

from aria.reading.exceptions import ReaderNotFoundError

from .suite import ParserTestCase, TempDirectoryTestCase, parse_from_path


class TestParserApi(ParserTestCase, TempDirectoryTestCase):
    def test_minimal_blueprint(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_type_section()
        self.template.node_template_section()
        result = self.parse()
        self._assert_minimal_blueprint(result)

    def test_import_from_path(self):
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.node_type_section()
        self.template.node_template_section()
        template_as_import = self.create_yaml_with_imports([str(self.template)])
        self.template.clear()
        self.template.version_section('cloudify_dsl', '1.0')
        self.template.template += template_as_import
        result = self.parse()
        self._assert_minimal_blueprint(result)

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

    def _assert_minimal_blueprint(self, result):
        self.assertEquals(1, len(result['nodes']))
        node = result['nodes'][0]
        self.assertEquals('test_node', node['id'])
        self.assertEquals('test_node', node['name'])
        self.assertEquals('test_type', node['type'])
        self.assertEquals('val', node['properties']['key'])
