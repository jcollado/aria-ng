
from aria import dsl_specification, has_validated_properties, validated_property
import tosca
    
@has_validated_properties
@dsl_specification('10.6.1', 'tosca-simple-nfv-1.0')
class VNFFG(object):
    """
    The NFV VNFFG group type represents a logical VNF forwarding graph entity as defined by [ETSI GS NFV-MAN 001 v1.1.1].
    
    See the `TOSCA Simple Profile for NFV v1.0 specification <http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/tosca-nfv-v1.0.html#_Toc447714727>`__
    """

    SHORTHAND_NAME = 'VNFFG' # spec is wrong here
    TYPE_QUALIFIED_NAME = 'tosca:VNFFG'
    TYPE_URI = 'tosca.groups.nfv.VNFFG'

    @validated_property(str, required=True)
    def vendor(self):
        """
        Specify the vendor generating this VNFFG.
        """

    @validated_property(tosca.Version, required=True)
    def version(self):
        """
        Specify the identifier (e.g. name), version, and description of service this VNFFG is describing.
        """

    @validated_property(tosca.Integer, required=True)
    def number_of_endpoints(self):
        """
        Count of the external endpoints included in this VNFFG, to form an index.
        """

    @validated_property(tosca.List(str), required=True)
    def dependent_virtual_link(self):
        """
        Reference to a list of VLD used in this Forwarding Graph.
        """

    @validated_property(tosca.List(str), required=True)
    def connection_point(self):
        """
        Reference to Connection Points forming the VNFFG.
        """

    @validated_property(tosca.List(str), required=True)
    def constituent_vnfs(self):
        """
        Reference to a list of  VNFD used in this VNF Forwarding Graph.
        """

__all__ = (
    'VNFFG',)
