import uuid
from causeweb.storage.db import DB
from causeweb.site.multilang import MultiLang
from causeweb.apis.base import Base
from .state import State


class Region(Base):
	table_name = 'tbl_region'
	mapping_method = {
		'GET': 'get',
		'PUT': 'create',
		'POST': 'modify',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_region=None, is_active=None):
		""" Return all region information

		:param id_region: UUID
		"""
		with DB() as db:
			if id_region is None and is_active is None:
				data = db.get_all("SELECT * FROM tbl_region;")
			elif id_region is None:
				data = db.get_all("SELECT * FROM tbl_region WHERE is_active=%s;", (is_active,))
			else:
				data = db.get_all("SELECT * FROM tbl_region WHERE id_region=%s;", (id_region,))

		for key, row in enumerate(data):
			data[key]['name'] = MultiLang.get(row['id_language_content_name'])
			data[key]['state'] = State().get(row['id_state'])

		return {
			'data': data
		} if id_region is None else data[0]

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

		id_region = uuid.uuid4()
		id_language_content = MultiLang.set(args['name'], True)

		with DB() as db:
			db.execute("""INSERT INTO tbl_region(
							id_region, code, id_language_content_name, id_state, is_active
						  ) VALUES(%s, %s, %s, %s, True);""", (
				id_region, args['code'], id_language_content, args['id_state']
			))

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

		id_language_content = MultiLang.set(args['name'])

		with DB() as db:
			db.execute("""UPDATE tbl_region
						SET code=%s, id_language_content_name=%s, id_state=%s, is_active=%s
						WHERE id_region=%s;""", (
			    args['code'], id_language_content, args['id_state'], args['is_active'], args['id_region']
			))

		return {
			'message': 'region successfully modify'
		}

	def remove(self, id_region):
		""" Remove a region

		:param id_region: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with DB() as db:
			db.execute("UPDATE tbl_region SET is_active=%s WHERE id_region=%s;", (
				False, id_region
			))

		return {
			'message': 'region successfully removed'
		}