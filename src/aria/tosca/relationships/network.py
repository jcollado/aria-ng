
from aria import dsl_specification, has_validated_properties
import tosca.relationships
	
@has_validated_properties
@dsl_specification('7.5.4', 'tosca-simple-profile-1.0')
class LinksTo(tosca.relationships.DependsOn):
	"""
	This relationship type represents an association relationship between Port and Network node types.
	
	See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_RELATIONSHIPS_NETWORK_LINKSTO>`__
	"""

	SHORTHAND_NAME = 'LinksTo'
	TYPE_QUALIFIED_NAME = 'tosca:LinksTo'
	TYPE_URI = 'tosca.relationships.network.LinksTo'

@has_validated_properties
@dsl_specification('7.5.5', 'tosca-simple-profile-1.0')
class BindsTo(tosca.relationships.DependsOn):
	"""
	This type represents a network association relationship between Port and Compute node types.
	
	See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_RELATIONSHIPS_NETWORK_BINDTO>`__
	"""

	SHORTHAND_NAME = 'BindsTo'
	TYPE_QUALIFIED_NAME = 'tosca:BindsTo'
	TYPE_URI = 'tosca.relationships.network.BindsTo'

__all__ = (
    'LinksTo',
    'BindsTo')
