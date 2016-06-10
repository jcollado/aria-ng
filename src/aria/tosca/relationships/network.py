
import tosca, tosca.relationships
	
class LinksTo(tosca.relationships.DependsOn):
	"""
	This relationship type represents an association relationship between Port and Network node types.
	
	See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_RELATIONSHIPS_NETWORK_LINKSTO>`__
	"""
	
	DESCRIPTION = 'This relationship type represents an association relationship between Port and Network node types.'

	SHORTHAND_NAME = 'LinksTo'
	TYPE_QUALIFIED_NAME = 'tosca:LinksTo'
	TYPE_URI = 'tosca.relationships.network.LinksTo'

class BindsTo(tosca.relationships.DependsOn):
	"""
	This type represents a network association relationship between Port and Compute node types.
	
	See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_TYPE_RELATIONSHIPS_NETWORK_BINDTO>`__
	"""
	
	DESCRIPTION = 'This type represents a network association relationship between Port and Compute node types.'

	SHORTHAND_NAME = 'BindsTo'
	TYPE_QUALIFIED_NAME = 'tosca:BindsTo'
	TYPE_URI = 'tosca.relationships.network.BindsTo'
