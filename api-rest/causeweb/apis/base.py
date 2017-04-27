from causeweb import config
from causeweb.storage.db import DB
from causeweb.session.static import Static as Session


if config.WEBSERVICE is not None:
	from ..site.permissionwebservice import PermissionWebService as onUsePermission
else:
	with DB() as db:
		if 'idpermission' in db.get_field('tbl_permission'):
			from ..cauca.geobase_permission import GeobasePermission as onUsePermission
		else:
			from ..site.permissiondb import PermissionDB as onUsePermission


class Base():
	table_name = ''
	mapping_method = {
		'GET': '',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def every_execution(self, method, *args):
		if self.table_name == '' or method == 'GET' or method == 'PUT':
			return

		table_id = self.table_name.replace('tbl_', 'id_')

		if table_id in args[0]:
			with DB() as db:
				db.execute("""INSERT INTO tbl_apis_action(
								id_apis_update, action_table, action_table_id, id_webuser
							  ) VALUES(uuid_generate_v4(), %s, %s, %s);""", (
					self.table_name, args[0][table_id], Session.get('userId')
				))

	def options(self):
		return {}

	def has_permission(self, feature_name):
		if onUsePermission().get(feature_name) is True:
			return True

		return False

	def no_access(self):
		return {
			'error': 'check your access'
		}