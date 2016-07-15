
from .. import merge
from .presentation import Presentation

class Presenter(Presentation):
    """
    Base class for ARIA presenters.
    
    Presenters provide a robust API over agnostic raw data.
    """

    def _get_import_locations(self):
        return []
    
    def _merge_import(self, presentation):
        merge(self._raw, presentation._raw)
        if hasattr(self._raw, '_locator') and hasattr(presentation._raw, '_locator'):
            self._raw._locator.merge(presentation._raw._locator)

    def _link(self):
        locator = self._raw._locator
        locator.link(self._raw)

    @property
    def deployment_plan(self):
        return None

    @property
    def repositories(self):
        return None

    @property
    def inputs(self):
        return None
            
    @property
    def outputs(self):
        return None

    @property
    def data_types(self):
        return None
    
    @property
    def node_types(self):
        return None
    
    @property
    def relationship_types(self):
        return None
    
    @property
    def group_types(self):
        return None

    @property
    def capability_types(self):
        return None

    @property
    def interface_types(self):
        return None

    @property
    def artifact_types(self):
        return None

    @property
    def policy_types(self):
        return None
    
    @property
    def node_templates(self):
        return None
    
    @property
    def relationship_templates(self):
        return None

    @property
    def groups(self):
        return None

    @property
    def workflows(self):
        return None
