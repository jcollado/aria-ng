
from aria import DSL_SPECIFICATION_PACKAGES
from aria.presentation import PRESENTER_CLASSES
from aria.loading import FILE_LOADER_PATHS
from .v1_0 import ToscaSimplePresenter1_0
import os.path

def install_aria_extension():
    # v1.0 presenter
    PRESENTER_CLASSES.append(ToscaSimplePresenter1_0)
    
    # DSL specification
    DSL_SPECIFICATION_PACKAGES.append('aria_extension_tosca')
    
    # Imports
    dir = os.path.dirname(os.path.dirname(__file__))
    FILE_LOADER_PATHS.append(os.path.join(dir, 'profiles'))

MODULES = (
    'v1_0',)

__all__ = (
    'MODULES',
    'install_aria_extension')
