import json
from ..manage.database import Database
from ..models.apis_action import ApisAction as Table


class Base:
	logged_id_webuser = None
	table_name = ''
	mapping_method = {
		'GET': '',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def every_execution(self, class_name, method, *args):
		if self.table_name == '':
			return

		field_id = self.table_name.replace('tbl_', 'id_')
		object_id = None

		if len(args) > 0:
			if field_id in args[0]:
				object_id = args[0][field_id]

		with Database() as db:
			db.insert(Table(Base.logged_id_webuser, method, json.dumps(args), class_name, object_id))
			db.commit()

	def options(self):
		return {}

	def has_permission(self, feature_name):
		#if onUsePermission().get(feature_name) is True:
		return True

		#return False

	def no_access(self):
		return {
			'error': 'check your access'
		}