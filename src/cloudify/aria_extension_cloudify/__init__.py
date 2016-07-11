
from aria.presentation import PRESENTER_CLASSES
from .v1_3 import CloudifyPresenter1_3

def install_aria_extension():
    PRESENTER_CLASSES.append(CloudifyPresenter1_3)

MODULES = (
    'v1_2',
    'v1_3')

__all__ = (
    'MODULES',
    'install_aria_extension')
