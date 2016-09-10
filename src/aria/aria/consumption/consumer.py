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

from .. import AriaError, Issue
from ..utils import print_exception

class Consumer(object):
    """
    Base class for ARIA consumers.
    
    Consumers provide useful functionality by consuming presentations.
    """
    
    def __init__(self, context):
        self.context = context
    
    def consume(self):
        pass
    
    def dump(self):
        pass

    def _handle_exception(self, e):
        if hasattr(e, 'issue') and isinstance(e.issue, Issue):
            self.context.validation.report(issue=e.issue)
        else:
            self.context.validation.report(exception=e)
        if not isinstance(e, AriaError):
            print_exception(e)

class ConsumerChain(Consumer):
    """
    ARIA consumer chain.
    
    Calls consumers in order, but stops if there are any validation issues along the way.
    """

    def __init__(self, context, consumer_classes=None):
        super(ConsumerChain, self).__init__(context)
        self.consumers = []
        if consumer_classes:
            for consumer_class in consumer_classes:
                self.append(consumer_class)
    
    def append(self, consumer_class):
        self.consumers.append(consumer_class(self.context))

    def consume(self):
        for consumer in self.consumers:
            consumer.consume()
            if self.context.validation.has_issues:
                break
