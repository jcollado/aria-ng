
from aria import import_modules, DSL_SPECIFICATION_PACKAGES
from aria.presentation import PRESENTER_CLASSES
from .v1_0 import ToscaSimplePresenter1_0

def install_aria_extension():
    PRESENTER_CLASSES.append(ToscaSimplePresenter1_0)
    DSL_SPECIFICATION_PACKAGES.append('tosca')

MODULES = (
    'v1_0',)

__all__ = (
    'MODULES',
    'install_aria_extension')
