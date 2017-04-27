import uuid
from causeweb.storage.db import DB
from causeweb.site.multilang import MultiLang
from causeweb.apis.base import Base
from .state import State


class County(Base):
	table_name = 'tbl_county'
	mapping_method = {
		'GET': 'get',
		'PUT': 'create',
		'POST': 'modify',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_county=None, is_active=None):
		""" Return all county information

		:param id_county: UUID
		:param id_active: BOOLEAN
		"""
		with DB() as db:
			if id_county is None and is_active is None:
				data = db.get_all("SELECT * FROM tbl_county;")
			elif id_county is None:
				data = db.get_all("SELECT * FROM tbl_county WHERE is_active=%s;", (is_active,))
			else:
				data = db.get_all("SELECT * FROM tbl_county WHERE id_county=%s;", (id_county,))

		for key, row in enumerate(data):
			data[key]['name'] = MultiLang.get(row['id_language_content_name'])
			data[key]['state'] = State().get(row['id_state'])

		return {
			'data': data
		} if id_county is None else data[0]


	def create(self, args):
		""" Create a new county

		:param args: {
			name: JSON,
			id_state: UUID
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		id_county = uuid.uuid4()
		id_language_content = MultiLang.set(args['name'], True)

		with DB() as db:
			db.execute("""INSERT INTO tbl_county(
							id_county, id_language_content_name, id_state, is_active
						  ) VALUES(%s, %s, %s, True);""", (
				id_county, id_language_content, args['id_state']
			))

		return {
			'id_county': id_county,
			'message': 'county successfully created'
		}

	def modify(self, args):
		""" Modify a county

		:param args: {
			id_county: UUID,
			name: JSON,
			id_state: UUID,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'id_county' not in args:
			raise Exception("You need to pass a id_county")

		id_language_content = MultiLang.set(args['name'])

		with DB() as db:
			db.execute("""UPDATE tbl_county
						SET id_language_content_name=%s, id_state=%s, is_active=%s
						WHERE id_county=%s;""", (
			    id_language_content, args['id_state'], args['is_active'], args['id_county']
			))

		return {
			'message': 'county successfully modify'
		}

	def remove(self, id_county):
		""" Remove a county

		:param id_county: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with DB() as db:
			db.execute("UPDATE tbl_county SET is_active=%s WHERE id_county=%s;", (
				False, id_county
			))

		return {
			'message': 'county successfully removed'
		}