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

from .parse import ParsingContext
from .validate import ValidationContext
from ..loading import LoadingContext
from ..reading import ReadingContext
from ..presentation import PresentationContext
from ..deployment import DeploymentContext
from .style import Style
import sys

class ConsumptionContext(object):
    def __init__(self):
        self.args = []
        self.out = sys.stdout
        self.style = Style()
        self.parsing = ParsingContext()
        self.validation = ValidationContext()
        self.loading = LoadingContext()
        self.reading = ReadingContext()
        self.presentation = PresentationContext()
        self.deployment = DeploymentContext()
