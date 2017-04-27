import uuid
from causeweb.storage.db import DB
from causeweb.site.multilang import MultiLang
from causeweb.apis.base import Base
from .county import County


class City(Base):
	table_name = 'tbl_city'
	mapping_method = {
		'GET': 'get',
		'PUT': 'create',
		'POST': 'modify',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_city=None, is_active=None):
		""" Return all city information

		:param id_city: UUID
		"""
		with DB() as db:
			if id_city is None and is_active is None:
				data = db.get_all("SELECT * FROM tbl_city;")
			elif id_city is None:
				data = db.get_all("SELECT * FROM tbl_city WHERE is_active=%s;", (is_active,))
			else:
				data = db.get_all("SELECT * FROM tbl_city WHERE id_city=%s;", (id_city,))

		for key, row in enumerate(data):
			data[key]['name'] = MultiLang.get(row['id_language_content_name'])

			if 'id_county' in row:
				data[key]['county'] = County().get(row['id_county'])

		return {
			'data': data
		} if id_city is None else data[0]

	def create(self, args):
		""" Create a new city

		:param args: {
			name: JSON,
			id_county: UUID,
			code: INTEGER,
			code_3_letter: STRING,
			email_address: STRING,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		id_city = uuid.uuid4()
		id_language_content = MultiLang.set(args['name'], True)

		with DB() as db:
			db.execute("""INSERT INTO tbl_city(
							id_city, id_language_content_name, id_county, code, code_3_letter, email_address, is_active
						  ) VALUES (%s, %s, %s, %s, %s, %s, True);""", (
				id_city, id_language_content, args['id_county'], args['code'], args['code_3_letter'], args['email_address']
			))

		return {
			'id_city': id_city,
			'message': 'city successfully created'
		}

	def modify(self, args):
		""" Modify a city

		:param args: {
			id_city: UUID,
			name: JSON,
			code: INTEGER,
			code_3_letter: STRING,
			email_address: STRING,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'id_city' not in args:
			raise Exception("You need to pass a id_city")

		id_language_content = MultiLang.set(args['name'])

		with DB() as db:
			db.execute("""UPDATE tbl_city SET
			           	id_language_content_name=%s, id_county=%s, code=%s, code_3_letter=%s, email_address=%s, is_active=%s
			           WHERE id_city=%s;""", (
				id_language_content, args['id_county'], args['code'], args['code_3_letter'], args['email_address'], args['is_active'], args['id_city']
			))

		return {
			'message': 'city successfully modify'
		}

	def remove(self, id_city):
		""" Remove a city

		:param id_city: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with DB() as db:
			db.execute("UPDATE tbl_city SET is_active=%s WHERE id_city=%s;", (
				False, id_city
			))

		return {
			'message': 'city successfully removed'
		}