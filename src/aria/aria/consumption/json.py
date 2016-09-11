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
from ..utils import json_dumps

class Json(Consumer):
    """
    Emits the presentation's raw data as JSON.
    """
    
    def dump(self):
        indent = self.context.get_arg_value_int('indent', 2)
        text = json_dumps(self.context.presentation.presenter._raw, indent=indent)
        self.context.out.write(text)
