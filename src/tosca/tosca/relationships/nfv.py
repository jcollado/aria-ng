
from aria import dsl_specification, has_validated_properties
import tosca.relationships
	
@has_validated_properties
@dsl_specification('8.4.1', 'tosca-simple-nfv-1.0')
class VirtualBindsTo(tosca.relationships.DependsOn):
	"""
	This relationship type represents an association relationship between VDU and CP node types.

    See the `TOSCA Simple Profile for NFV v1.0 specification <http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/tosca-nfv-v1.0.html#_Toc419290234>`__
	"""

	SHORTHAND_NAME = 'VirtualBindsTo'
	TYPE_QUALIFIED_NAME = 'tosca:VirtualBindsTo'
	TYPE_URI = 'tosca.relationships.nfv.VirtualBindsTo'

@has_validated_properties
@dsl_specification('8.4.2', 'tosca-simple-nfv-1.0')
class Monitor(tosca.relationships.ConnectsTo):
	"""
	This relationship type represents an association relationship to the Metric capability of VDU node types.

    See the `TOSCA Simple Profile for NFV v1.0 specification <http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/tosca-nfv-v1.0.html#_Toc418607880>`__
	"""

	SHORTHAND_NAME = 'Monitor'
	TYPE_QUALIFIED_NAME = 'tosca:Monitor'
	TYPE_URI = 'tosca.relationships.nfv.Monitor'

@has_validated_properties
@dsl_specification('10.4.1', 'tosca-simple-nfv-1.0')
class ForwardsTo(tosca.relationships.Root):
	"""
	This relationship type represents a traffic flow between two connection point node types.

    See the `TOSCA Simple Profile for NFV v1.0 specification <http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/tosca-nfv-v1.0.html#_Toc447714720>`__
	"""

	SHORTHAND_NAME = 'ForwardsTo'
	TYPE_QUALIFIED_NAME = 'tosca:ForwardsTo'
	TYPE_URI = 'tosca.relationships.nfv.ForwardsTo'

@has_validated_properties
@dsl_specification('11.4.1', 'tosca-simple-nfv-1.0')
class VirtualLinksTo(tosca.relationships.DependsOn):
	"""
	This relationship type represents an association relationship between VNFs and VL node types.

    See the `TOSCA Simple Profile for NFV v1.0 specification <http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/tosca-nfv-v1.0.html#_Toc447714737>`__
	"""

	SHORTHAND_NAME = 'VirtualLinksTo'
	TYPE_QUALIFIED_NAME = 'tosca:VirtualLinksTo'
	TYPE_URI = 'tosca.relationships.nfv.VirtualLinksTo'

__all__ = (
    'VirtualBindsTo',
    'Monitor',
    'ForwardsTo',
    'VirtualLinksTo')

