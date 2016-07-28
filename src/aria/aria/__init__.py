
from .issue import *
from .exceptions import *
from .specification import *
import pkgutil

VERSION = '0.1'

def install_aria_extensions():
    """
    Iterates all Python packages with names beginning with "aria\_extension\_" and calls
    their "install\_aria\_extension" function if they have it.
    """
    
    for loader, module_name, _ in pkgutil.iter_modules():
        if module_name.startswith('aria_extension_'):
            module = loader.find_module(module_name).load_module(module_name)
            
            if hasattr(module, 'install_aria_extension'):
                module.install_aria_extension()

            # Loading the module has contaminated sys.modules, so we'll clean it up
            del sys.modules[module_name]

MODULES = (
    'consumption',
    'deployment',
    'execution',
    'loading',
    'parsing',
    'presentation',
    'reading',
    'tools',
    'utils')

__all__ = (
    'MODULES',
    'VERSION',
    'install_aria_extensions',
    'Issue',
    'AriaError',
    'UnimplementedFunctionalityError',
    'InvalidValueError',
    'DSL_SPECIFICATION',
    'DSL_SPECIFICATION_PACKAGES',
    'dsl_specification',
    'iter_spec')
