import uuid
from causeweb.storage.db import DB
from causeweb.site.multilang import MultiLang
from causeweb.apis.base import Base


class CityType(Base):
	table_name = 'tbl_city_type'
	mapping_method = {
		'GET': 'get',
		'PUT': 'create',
		'POST': 'modify',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_city_type=None):
		""" Return all information for city type

		:param id_city_type: UUID
		"""
		with DB() as db:
			if id_city_type is None:
				data = db.get_all("SELECT * FROM tbl_city_type;")
			else:
				data = db.get_all("""SELECT * FROM tbl_city_type
                	                WHERE id_city_type=%s;""", (id_city_type,))

		for key, row in enumerate(data):
			data[key]['name'] = MultiLang.get(row['id_language_content_name'])

		return {
			'data': data
		} if id_city_type is None else data[0]

	def create(self, args):
		""" Create a new city type

		:param args: {
			name: JSON
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		id_city_type = uuid.uuid4()
		id_language_content = MultiLang.set(args['name'], True)

		with DB() as db:
			db.execute("""INSERT INTO tbl_city_type(
							id_city_type, id_language_content_name, is_active
						  ) VALUES (%s, %s, True);""", (
				id_city_type, id_language_content
			))

		return {
			'id_city_type': id_city_type,
			'message': 'city type successfully created'
		}

	def modify(self, args):
		""" Modify a city type

		:param args: {
			id_city_type: UUID,
			name: JSON,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'id_city_type' not in args:
			raise Exception("You need to pass a id_city_type")

		id_language_content = MultiLang.set(args['name'])

		with DB() as db:
			db.execute("""UPDATE tbl_city_type SET
			           	id_language_content_name=%s, is_active=%s
			           WHERE id_city_type=%s;""", (
				id_language_content, args['is_active'], args['id_city_type']
			))

		return {
			'message': 'city type successfully modify'
		}

	def remove(self, id_city_type):
		""" Remove a city type

		:param id_city_type: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with DB() as db:
			db.execute("UPDATE tbl_city_type SET is_active=%s WHERE id_city_type=%s;", (
				False, id_city_type
			))

		return {
			'message': 'city type successfully removed'
		}