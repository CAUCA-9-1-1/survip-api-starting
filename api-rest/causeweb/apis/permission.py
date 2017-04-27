from .. import config
from ..storage.db import DB
from .base import Base


if config.WEBSERVICE is not None:
	from ..site.permissionwebservice import PermissionWebService as onUsePermission
else:
	with DB() as db:
		if 'idpermission' in db.get_field('tbl_permission'):
			from ..cauca.geobase_permission import GeobasePermission as onUsePermission
		else:
			from ..site.permissiondb import PermissionDB as onUsePermission


class Permission(Base):
	active = False
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def __init__(self):
		if config.PERMISSION is None and config.WEBSERVICE is None:
			return None

		self.active = True

	def get(self, feature_name=None):
		if self.active is False:
			return None

		return {
			'data': onUsePermission().get(feature_name)
		}

	def get_id_permission_object(self, object_table, generic_id):
		if self.active is False:
			return None

		return onUsePermission().get_id_permission_object(object_table, generic_id)

	def get_id_permission_system_feature(self, feature_name):
		if self.active is False:
			return None

		return onUsePermission().get_id_permission_system_feature(feature_name)

	def create_permission(self, generic_id, id_permission_system_feature, access):
		if self.active is False:
			return None

		return onUsePermission().create_permission(generic_id, id_permission_system_feature, access)

	def modify_permission(self, id_permission, access):
		if self.active is False:
			return None

		return onUsePermission().modify_permission(id_permission, access)

	def create_permission_system_feature(self, description, default_value):
		if self.active is False:
			return None

		return onUsePermission().create_permission_system_feature(description, default_value)

	def create_permission_object(self, generic_id):
		if self.active is False:
			return None

		return onUsePermission().create_permission_object(generic_id)