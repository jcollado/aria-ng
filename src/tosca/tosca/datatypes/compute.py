
from aria import dsl_specification, has_validated_properties, validated_property
import tosca.datatypes

@has_validated_properties
@dsl_specification('8.3.1', 'tosca-simple-nfv-1.0')
class CPUAllocation(tosca.datatypes.Root):
    """
    Granular CPU allocation requirements for NFV workloads.

    See the `TOSCA Simple Profile for NFV v1.0 specification <http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/tosca-nfv-v1.0.html#TYPE_TOSCA_DATA_PORTINFO>`__ (wrong anchor)
    """

    SHORTHAND_NAME = 'CPUAllocation'
    TYPE_QUALIFIED_NAME = 'tosca:CPUAllocation'
    TYPE_URI = 'tosca.datatypes.compute.container.Container.Architecture.CPUAllocation' # mismatch with TOSCA Simple Profile
    
    @validated_property(str)
    def cpu_affinity(self):
        """
        Describes whether vCPU need to be pinned to dedicated CPU core or shared dynamically.
        """

    @validated_property(str)
    def thread_allocation(self):
        """
        Describe thread allocation requirement.
        """

    @validated_property(tosca.Integer)
    def socket_count(self):
        """
        Number of CPU sockets.
        """

    @validated_property(tosca.Integer)
    def core_count(self):
        """
        Number of cores per socket.
        """

    @validated_property(tosca.Integer)
    def thread_count(self):
        """
        Number of threads per core.
        """

@has_validated_properties
@dsl_specification('8.3.2', 'tosca-simple-nfv-1.0')
class NUMA(tosca.datatypes.Root):
    """
    Granular Non-Uniform Memory Access (NUMA) topology requirements for NFV workloads.

    See the `TOSCA Simple Profile for NFV v1.0 specification <http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/tosca-nfv-v1.0.html#_Toc447714697>`__
    """

    SHORTHAND_NAME = 'NUMA'
    TYPE_QUALIFIED_NAME = 'tosca:NUMA'
    TYPE_URI = 'tosca.datatypes.compute.container.Container.Architecture.NUMA' # mismatch with TOSCA Simple Profile

    @validated_property(tosca.Integer)
    def id(self):
        """
        CPU socket identifier.
        """

    @validated_property(tosca.Map(tosca.Integer))
    def vcpus(self):
        """
        List of specific host cpu numbers within a NUMA socket complex.

        TODO: need a new base type, with non-overlapping, positive value validation (exclusivity),
        """

    @validated_property(tosca.Size)
    def mem_size(self):
        """
        Size of memory allocated from this NUMA memory bank.
        """

__all__ = (
    'CPUAllocation',
    'NUMA')
