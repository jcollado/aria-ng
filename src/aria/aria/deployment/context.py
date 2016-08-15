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

from .ids import generate_long_id, generate_short_id
from ..utils import JSONValueEncoder, prune
from .hierarchy import TypeHierarchy
from clint.textui import puts
import json, itertools

class IdType(object):
    SERIAL = 0
    """
    Serial ID: an integer.
    """

    LOCALLY_UNIQUE = 1
    """
    Locally unique ID: 5 hex digits long.
    """
    
    UNIVERSALLY_UNIQUE = 2
    """
    Universally unique ID (UUID): 32 hex digits long.
    """

class DeploymentContext(object):
    def __init__(self):
        #self.id_type = IdType.SERIAL
        self.id_type = IdType.UNIVERSALLY_UNIQUE
        self.template = None
        self.plan = None
        self.node_types = TypeHierarchy()
        self.capability_types = TypeHierarchy()
        
        self._serial_id_counter = itertools.count(1)
        self._locally_unique_ids = set()
    
    def generate_id(self):
        if self.id_type == IdType.SERIAL:
            return self._serial_id_counter.next()
        elif self.id_type == IdType.LOCALLY_UNIQUE:
            the_id = generate_short_id()
            while the_id in self._locally_unique_ids:
                the_id = generate_short_id()
            self._locally_unique_ids.add(the_id)
            return the_id
        return generate_long_id()

    @property
    def plan_as_raw(self):
        raw = self.plan.as_raw
        prune(raw)
        return raw

    def get_plan_as_json(self, indent=None):
        raw = self.plan_as_raw
        return json.dumps(raw, indent=indent, cls=JSONValueEncoder)

    def dump_types(self, context):
        if self.node_types.children:
            puts('Node types:')
            self.node_types.dump(context)
        if self.capability_types.children:
            puts('Capability types:')
            self.capability_types.dump(context)
