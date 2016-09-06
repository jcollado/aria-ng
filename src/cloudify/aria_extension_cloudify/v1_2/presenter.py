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

from ..v1_1 import CloudifyPresenter1_1
from .templates import ServiceTemplate
from aria.utils import cachedmethod

class CloudifyPresenter1_2(CloudifyPresenter1_1):
    """
    ARIA presenter for the `Cloudify DSL v1.2 specification <http://docs.getcloudify.org/3.3.1/blueprints/overview/>`__.
    """

    @property
    @cachedmethod
    def service_template(self):
        return ServiceTemplate(raw=self._raw)

    # Presenter

    @staticmethod
    def can_present(raw):
        dsl = raw.get('tosca_definitions_version')
        return dsl == 'cloudify_dsl_1_2'
