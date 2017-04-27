from .. import config
from ..storage.db import DB
from .permission import Permission


if config.WEBSERVICE is not None:
	from ..site.permissionwebservice import PermissionWebService as onUsePermission
else:
	with DB() as db:
		if 'idpermission' in db.get_field('tbl_permission'):
			from ..cauca.geobase_permission import GeobasePermission as onUsePermission
		else:
			from ..site.permissiondb import PermissionDB as onUsePermission


class PermissionUser(Permission):
	active = False
	mapping_method = {
		'GET': 'get_all',
		'PUT': 'move',
		'POST': 'save',
		'DELETE': '',
		'PATCH': '',
	}

	def get_all(self, id_permission_object=None, object_table=None, generic_id=None):
		""" Return all user permission

		:param id_permission_object: UUID
		:param object_table: String
		:param generic_id: String
		"""
		if self.active is False:
			return None

		if id_permission_object is None and object_table is None and generic_id is None:
			return {
				'data': onUsePermission().get_object()
			}

		return {
			'data': onUsePermission().get_all(id_permission_object, object_table, generic_id)
		}

	def move(self, args):
		onUsePermission().set_permission_object_parent(args['id_permission_object'], args['id_permission_object_parent'])

		return {
			'message': 'permission object successfully move'
		}

	def save(self, args):
		if 'id_permission' not in args or args['id_permission'] is None:
			if 'id_permission_system_feature' not in args:
				args['id_permission_system_feature'] = self.create_permission_system_feature(args['description'], args['default_value'])

			if 'id_permission_object' not in args or args['id_permission_object'] is None:
				args['id_permission_object'] = self.get_id_permission_object(args['object_table'], args['generic_id'])

			self.create_permission(args['id_permission_object'], args['id_permission_system_feature'], args['access'])
		else:
			self.modify_permission(args['id_permission'], args['access'])

		return {
			'message': 'permission successfully save'
		}