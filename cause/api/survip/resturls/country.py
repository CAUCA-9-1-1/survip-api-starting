import uuid
from cause.api.management.core.database import Database
from cause.api.management.core.multilang import MultiLang
from cause.api.management.resturls.base import Base
from ..models.country import Country as Table


class Country(Base):
	table_name = 'tbl_country'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_country=None, is_active=None):
		""" Return all country information

		:param id_country: UUID
		:param id_active: BOOLEAN
		"""
		with Database() as db:
			if id_country is None and is_active is None:
				data = db.query(Table).all()
			elif id_country is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_country)

		return {
			'data': data
		}

	def create(self, args):
		""" Create a new country

		:param args: {
			name: JSON,
			code_alpha2: STRING,
			code_alpha3: STRING
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'name' not in args:
			raise Exception("You need to pass a 'name'")

		id_country = uuid.uuid4()
		id_language_content = MultiLang.set(args['name'], True)
		code_alpha2 = args['code_alpha2'] if 'code_alpha2' in args else None
		code_alpha3 = args['code_alpha3'] if 'code_alpha3' in args else None

		with Database() as db:
			db.insert(Table(id_country, id_language_content, code_alpha2, code_alpha3))
			db.commit()

		return {
			'id_country': id_country,
			'message': 'country successfully created'
		}

	def modify(self, args):
		""" Modify a country

		:param args: {
			id_country: UUID,
			name: JSON,
			code_alpha2: STRING,
			code_alpha3: STRING,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'id_country' not in args:
			raise Exception("You need to pass a id_country")

		with Database() as db:
			data = db.query(Table).get(args['id_country'])

			if 'name' in args:
				data.id_language_content_name = MultiLang.set(args['name'])

			if 'code_alpha2' in args:
				data.code_alpha2 = args['code_alpha2']
			if 'code_alpha3' in args:
				data.code_alpha3 = args['code_alpha3']
			if 'is_active' in args:
				data.is_active = args['is_active']

			db.commit();

		return {
			'message': 'country successfully modified'
		}

	def remove(self, id_country):
		""" Remove a country

		:param id_country: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_country)
			data.is_active = False
			db.commit()

		return {
			'message': 'country successfully removed'
		}