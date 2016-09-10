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

from .loader import Loader
from .exceptions import LoaderError, DocumentNotFoundError
import codecs, os.path

FILE_LOADER_SEARCH_PATHS = []

class FileTextLoader(Loader):
    """
    ARIA file text loader.
    
    Extracts a text document from a file. The default encoding is UTF-8, but other supported
    encoding can be specified instead.
    
    Supports a list of search paths that are tried in order if the file cannot be found.
    
    If :code:`origin_location` is provided, a base path will be extracted from it and prepended
    to the search paths.
    """

    def __init__(self, source, location, origin_location, encoding='utf-8'):
        self.source = source
        self.location = location
        self.encoding = encoding
        self.path = location.as_file
        self.search_paths = FILE_LOADER_SEARCH_PATHS
        self.file = None
        
        if origin_location is not None:
            origin_search_path = origin_location.search_path
            if origin_search_path is not None:
                self.search_paths = [origin_search_path] + self.search_paths
    
    def open(self):
        try:
            self._open(os.path.abspath(self.path))
        except IOError as e:
            if e.errno == 2:
                # Not found, so try in paths
                for p in self.search_paths:
                    path = os.path.join(p, self.path)
                    try:
                        self._open(path)
                        return
                    except IOError as e:
                        if e.errno != 2:
                            raise LoaderError('file I/O error: "%s"' % path, cause=e)
                raise DocumentNotFoundError('file not found: "%s"' % self.location, cause=e)
            else:
                raise LoaderError('file I/O error: "%s"' % self.location, cause=e)
        except Exception as e:
            raise LoaderError('file error: "%s"' % self.location, cause=e)

    def close(self):
        if self.file is not None:
            try:
                self.file.close()
            except IOError as e:
                raise LoaderError('file I/O error: "%s"' % self.location, cause=e)
            except Exception as e:
                raise LoaderError('file error: "%s"' % self.location, cause=e)

    def load(self):
        if self.file is not None:
            try:
                return self.file.read()
            except IOError as e:
                raise LoaderError('file I/O error: "%s"' % self.location, cause=e)
            except Exception as e:
                raise LoaderError('file error %s' % self.location, cause=e)
        return None

    def _open(self, path):
        self.file = codecs.open(path, mode='r', encoding=self.encoding, buffering=1)
        self.location.uri = path
