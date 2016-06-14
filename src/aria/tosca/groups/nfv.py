
from aria import has_validated_properties, validated_property, property_type, property_default, required_property
import tosca
    
@has_validated_properties
class VNFFG(object):
    """
    The NFV VNFFG group type represents a logical VNF forwarding graph entity as defined by [ETSI GS NFV-MAN 001 v1.1.1].
    
    See the `TOSCA Simple Profile for NFV v1.0 specification <http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/tosca-nfv-v1.0.html#_Toc447714727>`__
    """

    SHORTHAND_NAME = 'VNFFG' # spec is wrong here
    TYPE_QUALIFIED_NAME = 'tosca:VNFFG'
    TYPE_URI = 'tosca.groups.nfv.VNFFG'

    @required_property
    @property_type(str)
    @validated_property
    def vendor():
        """
        Specify the vendor generating this VNFFG.
        """

    @required_property
    @property_type(tosca.Version)
    @validated_property
    def version():
        """
        Specify the identifier (e.g. name), version, and description of service this VNFFG is describing.
        """

    @required_property
    @property_type(tosca.Integer)
    @validated_property
    def number_of_endpoints():
        """
        Count of the external endpoints included in this VNFFG, to form an index.
        """

    @required_property
    @property_type(tosca.List(str))
    @validated_property
    def dependent_virtual_link():
        """
        Reference to a list of VLD used in this Forwarding Graph.
        """

    @required_property
    @property_type(tosca.List(str))
    @validated_property
    def connection_point():
        """
        Reference to Connection Points forming the VNFFG.
        """

    @required_property
    @property_type(tosca.List(str))
    @validated_property
    def constituent_vnfs():
        """
        Reference to a list of  VNFD used in this VNF Forwarding Graph.
        """
