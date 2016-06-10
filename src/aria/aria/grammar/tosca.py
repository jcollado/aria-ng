
__name__ = 'tosca_'

import aria.grammar
import tosca

class ToscaSimpleProfileGrammarV1_0(aria.grammar.Grammar):
    """
    ARIA grammar for `TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html>`.
    """
    
    @property
    def profile(self):
        return tosca.Profile(self.structure)

    def get_import_locators(self):
        return [i.file for i in self.profile.imports]
