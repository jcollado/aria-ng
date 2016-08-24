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

from .exceptions import LoaderNotFoundError
from .location import LiteralLocation, UriLocation
from .literal import LiteralLoader
from .file import FileTextLoader
from .uri import UriTextLoader
import os.path

class LoaderSource(object):
    """
    Base class for ARIA loader sources.
    
    Loader sources provide appropriate :class:`Loader` instances for locations.
    
    A :class:`LiteralLocation` is handled specially by wrapping the literal value
    in a :class:`LiteralLoader`.
    """
    
    def get_loader(self, location, origin_location):
        if isinstance(location, LiteralLocation):
            return LiteralLoader(location)
        
        raise LoaderNotFoundError('location: %s' % location)

class DefaultLoaderSource(LoaderSource):
    """
    The default ARIA loader source will generate a :class:`UriTextLoader` for
    locations that are non-file URIs, and a :class:`FileTextLoader` for file
    URIs and other strings.
    
    If :class:`FileTextLoader` is used, a base path will be extracted from
    :code:`origin_location`.
    """
    
    def get_loader(self, location, origin_location):
        if origin_location is not None:
            if isinstance(origin_location, UriLocation):
                origin_file = origin_location.as_file
                if origin_file is not None:
                    # It's a file, so include its base path
                    path = os.path.dirname(origin_file)
                    if path not in location.paths:
                        location.paths.insert(0, path)

            for path in origin_location.paths:
                if path not in location.paths:
                    location.paths.append(path)
            
        if isinstance(location, UriLocation):
            if location.as_file is not None:
                return FileTextLoader(self, location)
            else:
                return UriTextLoader(self, location)
            
        return super(DefaultLoaderSource, self).get_loader(location, origin_location)
