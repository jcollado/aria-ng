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

from .. import AriaError, UnimplementedFunctionalityError, Issue
from ..utils import classname, print_exception

class Consumer(object):
    """
    
    Base class for ARIA consumers.
    
    Consumers provide useful functionality by consuming presentations.
    
    """
    
    def __init__(self, context):
        self.context = context
    
    def consume(self):
        raise UnimplementedFunctionalityError(classname(self) + '.consume')

    def _handle_exception(self, e):
        if hasattr(e, 'issue') and isinstance(e.issue, Issue):
            self.context.validation.report(issue=e.issue)
        else:
            self.context.validation.report(exception=e)
        if not isinstance(e, AriaError):
            print_exception(e)
