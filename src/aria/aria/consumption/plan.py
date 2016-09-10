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

from .consumer import Consumer
from ..loading import UriLocation, LiteralLocation
from ..reading import JsonReader

class Inputs(object):
    def __init__(self, context, payload):
        if payload.endswith('.json') or payload.endswith('.yaml'):
            location = UriLocation(payload)
        else:
            location = LiteralLocation(payload)

        loader = context.loading.loader_source.get_loader(location, None)
        
        if isinstance(location, LiteralLocation):
            reader = JsonReader(context.reading, location, loader)
        else:
            reader = context.reading.reader_source.get_reader(context.reading, location, loader)
        
        raw = reader.read()
        print raw

class Plan(Consumer):
    """
    Generates the deployment plan by instantiating the deployment template.
    """

    def consume(self):
        if self.context.deployment.template is None:
            return

        for arg in self.context.args:
            if arg.startswith('--inputs='):
                inputs = arg[len('--inputs='):]
                inputs = Inputs(self.context, inputs)
                exit()

        try:
            if not self.context.validation.has_issues:
                self.context.deployment.template.instantiate(self.context, None)
            if not self.context.validation.has_issues:
                self.context.deployment.plan.validate(self.context)
            if not self.context.validation.has_issues:
                self.context.deployment.plan.satisfy_requirements(self.context)
            if not self.context.validation.has_issues:
                self.context.deployment.template.coerce_values(self.context, None, True)
            if not self.context.validation.has_issues:
                self.context.deployment.plan.validate_capabilities(self.context)
        except Exception as e:
            self._handle_exception(e)
    
    def dump(self):
        if self.context.deployment.plan is None:
            return
        
        if '--graph' in self.context.args:
            self.context.deployment.plan.dump_graph(self.context)
        elif '--yaml' in self.context.args:
            print self.context.deployment.get_plan_as_yaml(indent=2)
        elif '--json' in self.context.args:
            print self.context.deployment.get_plan_as_json(indent=2)
        else:
            self.context.deployment.plan.dump(self.context)
