import uuid
from causeweb.storage.db import DB
from causeweb.site.multilang import MultiLang
from causeweb.apis.base import Base


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
		with DB() as db:
			if id_country is None and is_active is None:
				data = db.get_all("SELECT * FROM tbl_country;")
			elif id_country is None:
				data = db.get_all("SELECT * FROM tbl_country WHERE is_active=%s;", (is_active,))
			else:
				data = db.get_all("SELECT * FROM tbl_country WHERE id_country=%s;", (id_country,))

		for key, row in enumerate(data):
			data[key]['name'] = MultiLang.get(row['id_language_content_name'])

		return {
			'data': data
		} if id_country is None else data[0]

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

		id_country = uuid.uuid4()
		id_language_content = MultiLang.set(args['name'], True)

		with DB() as db:
			db.execute("""INSERT INTO tbl_country(
							id_country, id_language_content_name, code_alpha2, code_alpha3, is_active
						  ) VALUES(%s, %s, %s, %s, True);""", (
				id_country, id_language_content, args['code_alpha2'], args['code_alpha3']
			))

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

		id_language_content = MultiLang.set(args['name'])

		with DB() as db:
			db.execute("""UPDATE tbl_country SET
							id_language_content_name=%s, code_alpha2=%s, code_alpha3=%s, is_active=%s
						WHERE id_country=%s;""", (
				id_language_content, args['code_alpha2'], args['code_alpha3'], args['is_active'], args['id_country']
			))

		return {
			'message': 'country successfully modify'
		}

	def remove(self, id_country):
		""" Remove a country

		:param id_country: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with DB() as db:
			db.execute("UPDATE tbl_country SET is_active=%s WHERE id_country=%s;", (
				False, id_country
			))

		return {
			'message': 'country successfully removed'
		}