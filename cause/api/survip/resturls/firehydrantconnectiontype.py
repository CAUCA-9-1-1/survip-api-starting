import uuid

from api.management.core.database import Database
from api.management.core.multilang import MultiLang
from cause.api.management.resturls.base import Base
from ..models.fire_hydrant_connection_type import FireHydrantConnectionType as Table


class FireHydrantConnectionType(Base):
	table_name = 'tbl_fire_hydrant_connection_type'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_fire_hydrant_connection_type=None, is_active=None):
		""" Return all information for fire hydrant connection type

		:param id_fire_hydrant_connection_type: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_fire_hydrant_connection_type is None and is_active is None:
				data = db.query(Table).all()
			elif id_fire_hydrant_connection_type is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_fire_hydrant_connection_type)

		return {
			'data': data
		}


	def create(self, args):
		""" Create a new fire hydrant connection type

		:param args: {
			name: JSON
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'name' not in args:
			raise Exception("You need to pass a 'name'")

		id_fire_hydrant_connection_type = uuid.uuid4()
		id_language_content = MultiLang.set(args['name'], True)

		with Database() as db:
			db.insert(Table(id_fire_hydrant_connection_type, id_language_content))
			db.commit()

		return {
			'id_fire_hydrant_connection_type': id_fire_hydrant_connection_type,
			'message': 'fire hydrant connection type successfully created'
		}

	def modify(self, args):
		""" Modify a fire hydrant connection type

		:param args: {
			id_fire_hydrant_connection_type: UUID,
			name: JSON,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'id_fire_hydrant_connection_type' not in args:
			raise Exception("You need to pass a id_fire_hydrant_connection_type")

		with Database() as db:
			data = db.query(Table).get(args['id_fire_hydrant_connection_type'])

			if 'name' in args:
				data.id_language_content_name = MultiLang.set(args['name'])
			if 'is_active' in args:
				data.is_active = args['is_active']

			db.commit()

		return {
			'message': 'fire hydrant connection type successfully modified'
		}

	def remove(self, id_fire_hydrant_connection_type):
		""" Remove a fire hydrant connection type

		:param id_fire_hydrant_connection_type: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_fire_hydrant_connection_type)
			data.is_active = False
			db.commit()

		return {
			'message': 'fire hydrant connection type successfully removed'
		}