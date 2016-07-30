
#
# Needs to be in its own file to avoid Python import loops
#

from aria.presentation import AsIsPresentation
from clint.textui import puts

class Description(AsIsPresentation):
    """
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
    """

    def _dump(self, context):
        puts(context.style.meta(self.value))
