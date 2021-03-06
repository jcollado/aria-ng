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

from aria import InvalidValueError

def data_type_class_getter(cls):
    """
    Wraps the field value in a specialized data type class.

    Can be used with the :func:`field_getter` decorator.
    """
    
    def getter(field, presentation):
        raw = field._get(presentation)
        if raw is not None:
            try:
                return cls(None, None, raw, None)
            except ValueError as e:
                raise InvalidValueError('%s is not a valid "%s.%s" in "%s": %s' % (field.fullname, cls.__module__, cls.__name__, presentation._name, repr(raw)), cause=e, locator=field.get_locator(raw))
    return getter
