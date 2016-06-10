
import aria.presenter.tosca_simple

class CloudifyPresenter1_3(aria.presenter.tosca_simple.ToscaSimplePresenter1_0):
    """
    ARIA presenter for Cloudify.
    """

    @staticmethod
    def can_present(raw):
        return raw.get('tosca_definitions_version') == 'cloudify_dsl_1_3'

    @property
    def profile(self):
        return Profile(self.raw)

class Profile(aria.presenter.tosca_simple.Profile):
    @property
    def node_templates(self):
        """
        :class:`NodeTemplate`
        """
        return self._get_object_dict('node_templates', aria.presenter.tosca_simple.NodeTemplate)

__all__ = [
    'CloudifyPresenter1_3',
    'Profile']
