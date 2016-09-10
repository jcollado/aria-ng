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

from .. import install_aria_extensions
from ..consumption import ConsumerChain, Presentation, Validation, Template, Inputs, Plan
from ..utils import JSONValueEncoder, print_exception
from ..loading import FILE_LOADER_PATHS, LiteralLocation
from .utils import CommonArgumentParser, create_context_ns
from rest_server import Config, start_server
from collections import OrderedDict
import urllib

API_VERSION = 1
PATH_PREFIX = 'openoapi/tosca/v%d' % API_VERSION
VALIDATE_PATH = '%s/validate' % PATH_PREFIX
PLAN_PATH = '%s/plan' % PATH_PREFIX

args = None

def validate(uri):
    context = create_context_ns(args, uri=uri)
    ConsumerChain(context, (Presentation, Validation)).consume()
    return context

def plan(uri):
    context = create_context_ns(args, uri=uri)
    ConsumerChain(context, (Presentation, Validation, Template, Inputs, Plan)).consume()
    return context

def issues(context):
    return {'issues': [i.as_raw for i in context.validation.issues]}

def validate_get(handler):
    path = urllib.unquote(handler.path[len(VALIDATE_PATH) + 2:])
    context = validate(path)
    return issues(context) if context.validation.has_issues else {}

def validate_post(handler):
    payload = handler.get_payload()
    context = validate(LiteralLocation(payload))
    return issues(context) if context.validation.has_issues else {}

def plan_get(handler):
    path = urllib.unquote(handler.path[len(PLAN_PATH) + 2:])
    context = plan(path)
    return issues(context) if context.validation.has_issues else context.deployment.plan_as_raw

def plan_post(handler):
    payload = handler.get_payload()
    context = plan(LiteralLocation(payload))
    return issues(context) if context.validation.has_issues else context.deployment.plan_as_raw

ROUTES = OrderedDict((
    ('^/$', {'file': 'index.html', 'media_type': 'text/html'}),
    ('^/' + VALIDATE_PATH, {'GET': validate_get, 'POST': validate_post, 'media_type': 'application/json'}),
    ('^/' + PLAN_PATH, {'GET': plan_get, 'POST': plan_post, 'media_type': 'application/json'})))

class ArgumentParser(CommonArgumentParser):
    def __init__(self):
        super(ArgumentParser, self).__init__(description='REST Server', prog='aria-rest')
        self.add_argument('--port', type=int, default=8204, help='HTTP port')
        self.add_argument('--root', default='.', help='web root directory')
        self.add_argument('--path', nargs='*', help='paths for imports')

def main():
    try:
        install_aria_extensions()
        
        global args
        args, _ = ArgumentParser().parse_known_args()
        if args.path:
            for path in args.path:
                FILE_LOADER_PATHS.append(path)
            
        config = Config()
        config.port = args.port
        config.routes = ROUTES
        config.static_root = args.root
        config.json_encoder = JSONValueEncoder(separators=(',',':'))
        
        start_server(config)

    except Exception as e:
        print_exception(e)

if __name__ == '__main__':
    main()
