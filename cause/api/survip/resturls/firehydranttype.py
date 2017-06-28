import uuid
from framework.manage.database import Database
from framework.manage.multilang import MultiLang
from framework.resturls.base import Base
from ..models.fire_hydrant_type import FireHydrantType as Table


class FireHydrantType(Base):
	table_name = 'tbl_fire_hydrant_type'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_fire_hydrant_type=None, is_active=None):
		""" Return all information for fire hydrant type

		:param id_fire_hydrant_type: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_fire_hydrant_type is None and is_active is None:
				data = db.query(Table).all()
			elif id_fire_hydrant_type is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_fire_hydrant_type)

		return {
			'data': data
		}


	def create(self, args):
		""" Create a new fire hydrant type

		:param args: {
			name: JSON
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'name' not in args:
			raise Exception("You need to pass a 'name'")

		id_fire_hydrant_type = uuid.uuid4()
		id_language_content = MultiLang.set(args['name'], True)

		with Database() as db:
			db.insert(Table(id_fire_hydrant_type, id_language_content))
			db.commit()

		return {
			'id_fire_hydrant_type': id_fire_hydrant_type,
			'message': 'fire hydrant type successfully created'
		}

	def modify(self, args):
		""" Modify a fire hydrant type

		:param args: {
			id_fire_hydrant_type: UUID,
			name: JSON,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'id_fire_hydrant_type' not in args:
			raise Exception("You need to pass a id_fire_hydrant_type")

		with Database() as db:
			data = db.query(Table).get(args['id_fire_hydrant_type'])

			if 'name' in args:
				data.id_language_content_name = MultiLang.set(args['name'])
			if 'is_active' in args:
				data.is_active = args['is_active']

			db.commit()

		return {
			'message': 'fire hydrant type successfully modified'
		}

	def remove(self, id_fire_hydrant_type):
		""" Remove a fire hydrant type

		:param id_fire_hydrant_type: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_fire_hydrant_type)
			data.is_active = False
			db.commit()

		return {
			'message': 'fire hydrant type successfully removed'
		}