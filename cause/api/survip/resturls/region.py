import uuid
from cause.api.management.core.manage.database import Database
from cause.api.management.core.manage.multilang import MultiLang
from cause.api.management.resturls.base import Base
from ..models.region import Region as Table


class Region(Base):
	table_name = 'tbl_region'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_region=None, is_active=None):
		""" Return all region information

		:param id_region: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_region is None and is_active is None:
				data = db.query(Table).all()
			elif id_region is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_region)

		return {
			'data': data
		}

	def create(self, args):
		""" Create a new region

		:param args: {
			code: INTEGER,
			name: JSON,
			id_state: UUID
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'id_state' not in args or 'name' not in args:
			raise Exception("You need to pass a 'name' and 'id_state'")

		id_region = uuid.uuid4()
		id_language_content = MultiLang.set(args['name'], True)
		code = args['code'] if 'code' in args else None

		with Database() as db:
			db.insert(Table(id_region, id_language_content, args['id_state'], code))
			db.commit()

		return {
			'id_region': id_region,
			'message': 'region successfully created'
		}

	def modify(self, args):
		""" Modify a region

		:param args: {
			id_region: UUID,
			code: INTEGER,
			name: JSON,
			id_state: UUID,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'id_region' not in args:
			raise Exception("You need to pass a id_region")

		with Database() as db:
			data = db.query(Table).get(args['id_region'])

			if 'name' in args:
				data.id_language_content_name = MultiLang.set(args['name'])
			if 'id_state' in args:
				data.id_state = args['id_state']
			if 'code' in args:
				data.code = args['code']
			if 'is_active' in args:
				data.is_active = args['is_active']

			db.commit()

		return {
			'message': 'region successfully modified'
		}

	def remove(self, id_region):
		""" Remove a region

		:param id_region: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_region)
			data.is_active = False
			db.commit()

		return {
			'message': 'region successfully removed'
		}