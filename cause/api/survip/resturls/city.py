import uuid

from api.management.core.database import Database
from api.management.core.multilang import MultiLang
from cause.api.management.resturls.base import Base
from ..models.city import City as Table


class City(Base):
	table_name = 'tbl_city'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_city=None, is_active=None):
		""" Return all city information

		:param id_city: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_city is None and is_active is None:
				data = db.query(Table).all()
			elif id_city is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_city)

		return {
			'data': data
		}

	def create(self, args):
		""" Create a new city

		:param args: {
			name: JSON,
			id_building: UUID,
			id_city_type: UUID,
			id_county: UUID,
			code: INTEGER,
			code3_letter: STRING,
			email_address: STRING,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'id_county' not in args or 'name' not in args:
			raise Exception("You need to pass a 'name' and 'id_county'")

		id_city = uuid.uuid4()
		id_language_content = MultiLang.set(args['name'], True)
		id_building = args['id_building'] if 'id_building' in args else None
		id_city_type = args['id_city_type'] if 'id_city_type' in args else None
		code = args['code'] if 'code' in args else None
		code3_letter = args['code3_letter'] if 'code3_letter' in args else None
		email_address = args['email_address'] if 'email_address' in args else None

		with Database() as db:
			db.insert(Table(
				id_city, id_language_content, id_building, args['id_county'], id_city_type,
				code, code3_letter, email_address))
			db.commit()

		return {
			'id_city': id_city,
			'message': 'city successfully created'
		}

	def modify(self, args):
		""" Modify a city

		:param args: {
			id_city: UUID,
			id_county: UUID,
			id_building: UUID,
			name: JSON,
			code: INTEGER,
			code3_letter: STRING,
			email_address: STRING,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'id_city' not in args:
			raise Exception("You need to pass a id_city")

		with Database() as db:
			data = db.query(Table).get(args['id_city'])

			if 'name' in args:
				data.id_language_content_name = MultiLang.set(args['name'])
			if 'id_building' in args:
				data.id_building = args['id_building']
			if 'id_city_type' in args:
				data.id_city_type = args['id_city_type']
			if 'id_county' in args:
				data.id_county = args['id_county']
			if 'code' in args:
				data.code = args['code']
			if 'code3_letter' in args:
				data.code3_letter = args['code3_letter']
			if 'is_active' in args:
				data.is_active = args['is_active']

			db.commit()

		return {
			'message': 'city successfully modified'
		}

	def remove(self, id_city):
		""" Remove a city

		:param id_city: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_city)
			data.is_active = False
			db.commit()

		return {
			'message': 'city successfully removed'
		}