
import aria.grammar.tosca_simple

class CloudifyGrammar1_3(aria.grammar.tosca_simple.ToscaSimpleGrammar1_0):
    """
    ARIA grammar for Cloudify.
    """

    @property
    def profile(self):
        return Profile(self.structure)

class Profile(aria.grammar.tosca_simple.Profile):
    @property
    def node_templates(self):
        """
        :class:`NodeTemplate`
        """
        return self._get_object_dict('node_templates', aria.grammar.tosca_simple.NodeTemplate)
