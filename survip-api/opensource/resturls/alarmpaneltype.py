import uuid
from framework.manage.database import Database
from framework.manage.multilang import MultiLang
from framework.resturls.base import Base
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

	def get(self, id_alarm_panel=None, is_active=None):
		""" Return all alarm panel information

		:param id_alarm_panel: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_alarm_panel is None and is_active is None:
				data = db.query(Table).all()
			elif id_alarm_panel is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_alarm_panel)

		return {
			'data': data
		}

	def create(self, args):
		""" Create a new alarm panel

		:param args: {
			name: JSON,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'name' not in args:
			raise Exception("You need to pass a 'name'")

		id_alarm_panel = uuid.uuid4()
		id_language_content = MultiLang.set(args['name'], True)

		with Database() as db:
			db.insert(Table(id_alarm_panel, id_language_content))
			db.commit()

		return {
			'id_alarm_panel': id_alarm_panel,
			'message': 'alarm panel successfully created'
		}

	def modify(self, args):
		""" Modify a alarm panel

		:param args: {
			id_alarm_panel: UUID,
			name: JSON,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'id_alarm_panel' not in args:
			raise Exception("You need to pass a id_alarm_panel")

		with Database() as db:
			data = db.query(Table).get(args['id_alarm_panel'])

			if 'name' in args:
				data.id_language_content_name = MultiLang.set(args['name'])
			if 'is_active' in args:
				data.is_active = args['is_active']

			db.commit()

		return {
			'message': 'alarm panel successfully modified'
		}

	def remove(self, id_alarm_panel):
		""" Remove a alarm panel

		:param id_alarm_panel: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_alarm_panel)
			data.is_active = False
			db.commit()

		return {
			'message': 'alarm panel successfully removed'
		}