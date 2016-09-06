#
# Copyright (c) 2016 GigaSpaces Technologies Ltd. All rights reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#

from ..v1_0 import NodeTemplate as NodeTemplate1_0, ServiceTemplate as ServiceTemplate1_0
from .utils.node_templates import get_node_template_scalable
from .misc import Instances
from aria import dsl_specification
from aria.presentation import has_fields, object_field, object_dict_field
from aria.utils import cachedmethod

@has_fields
@dsl_specification('node-templates-1', 'cloudify-1.2')
class NodeTemplate(NodeTemplate1_0):
    @object_field(Instances)
    def instances(self):
        """
        Instances configuration. (Deprecated. Replaced by :code:`capabilities.scalable`.)
        
        :rtype: :class:`Instances`
        """

    @cachedmethod
    def _get_scalable(self, context):
        return get_node_template_scalable(context, self)

    def _validate(self, context):
        super(NodeTemplate, self)._validate(context)
        self._get_scalable(context)

@has_fields
class ServiceTemplate(ServiceTemplate1_0):
    @object_dict_field(NodeTemplate)
    def node_templates(self):
        """
        :rtype: dict of str, :class:`NodeTemplate`
        """
