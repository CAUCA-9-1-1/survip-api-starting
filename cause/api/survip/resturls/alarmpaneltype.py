import uuid
from cause.api.management.core.database import Database
from cause.api.management.core.multilang import MultiLang
from cause.api.management.resturls.base import Base
from ..models.alarm_panel_type import AlarmPanelType as Table


class AlarmPanelType(Base):
	table_name = 'tbl_alarm_panel_type'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_alarm_panel_type=None, is_active=None):
		""" Return all alarm panel type information

		:param id_alarm_panel_type: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_alarm_panel_type is None and is_active is None:
				data = db.query(Table).all()
			elif id_alarm_panel_type is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_alarm_panel_type)

		return {
			'data': data
		}

	def create(self, args):
		""" Create a new alarm panel type

		:param args: {
			name: JSON,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'name' not in args:
			raise Exception("You need to pass a 'name'")

		id_alarm_panel_type = uuid.uuid4()
		id_language_content = MultiLang.set(args['name'], True)

		with Database() as db:
			db.insert(Table(id_alarm_panel_type, id_language_content))
			db.commit()

		return {
			'id_alarm_panel_type': id_alarm_panel_type,
			'message': 'alarm panel type successfully created'
		}

	def modify(self, args):
		""" Modify a alarm panel type

		:param args: {
			id_alarm_panel_type: UUID,
			name: JSON,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'id_alarm_panel_type' not in args:
			raise Exception("You need to pass a id_alarm_panel_type")

		with Database() as db:
			data = db.query(Table).get(args['id_alarm_panel_type'])

			if 'name' in args:
				data.id_language_content_name = MultiLang.set(args['name'])
			if 'is_active' in args:
				data.is_active = args['is_active']

			db.commit()

		return {
			'message': 'alarm panel type successfully modified'
		}

	def remove(self, id_alarm_panel_type):
		""" Remove a alarm panel type

		:param id_alarm_panel_type: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_alarm_panel_type)
			data.is_active = False
			db.commit()

		return {
			'message': 'alarm panel type successfully removed'
		}