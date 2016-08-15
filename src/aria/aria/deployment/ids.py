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

from shortuuid import ShortUUID
from random import randrange

# See: https://github.com/stochastic-technologies/shortuuid
UUID = ShortUUID() # default alphabet is base57, which is alphanumeric without visually ambiguous characters; ID length is 22
#UUID = ShortUUID(alphabet='01234567890ABCDEF') # hex characters; ID length is 32

def generate_long_id():
    """
    An ID with a strong guarantee of universal uniqueness.
    """
    
    return UUID.uuid()

def generate_short_id():
    """
    An ID with a weak guarantee of universal uniqueness.
    """

    return '%05x' % randrange(16 ** 5)
