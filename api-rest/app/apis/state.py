import uuid
from causeweb.storage.db import DB
from causeweb.site.multilang import MultiLang
from causeweb.apis.base import Base
from .country import Country


class State(Base):
	table_name = 'tbl_state'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_state=None, is_active=None):
		""" Return all state information

		:param id_state: UUID
		:param id_active: BOOLEAN
		"""
		with DB() as db:
			if id_state is None and is_active is None:
				data = db.get_all("SELECT * FROM tbl_state;")
			elif id_state is None:
				data = db.get_all("SELECT * FROM tbl_state WHERE is_active=%s;", (is_active,))
			else:
				data = db.get_all("SELECT * FROM tbl_state WHERE id_state=%s;", (id_state,))

		for key, row in enumerate(data):
			data[key]['name'] = MultiLang.get(row['id_language_content_name'])
			data[key]['country'] = Country().get(row['id_country'])

		return {
			'data': data
		} if id_state is None else data[0]

	def create(self, args):
		""" Create a new state

		:param args: {
			name: JSON,
			id_country: UUID,
			ansi_code: STRING,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		id_state = uuid.uuid4()
		id_language_content = MultiLang.set(args['name'], True)

		with DB() as db:
			db.execute("""INSERT INTO tbl_state(
							id_state, id_language_content_name, id_country, ansi_code, is_active
						  ) VALUES(%s, %s, %s, %s, True);""", (
				id_state, id_language_content, args['id_country'], args['ansi_code']
			))

		return {
			'id_state': id_state,
			'message': 'state successfully created'
		}

	def modify(self, args):
		""" Modify a state

		:param args: {
			id_state: UUID,
			name: JSON,
			id_country: UUID,
			ansi_code: STRING,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'id_state' not in args:
			raise Exception("You need to pass a id_state")

		id_language_content = MultiLang.set(args['name'])

		with DB() as db:
			db.execute("""UPDATE tbl_state
						SET id_language_content_name=%s, id_country=%s, ansi_code=%s, is_active=%s
						WHERE id_state=%s;""", (
				id_language_content, args['id_country'], args['ansi_code'], args['is_active'], args['id_state']
			))

		return {
			'message': 'state successfully modify'
		}

	def remove(self, id_state):
		""" Remove a state

		:param id_state: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with DB() as db:
			db.execute("UPDATE tbl_state SET is_active=%s WHERE id_state=%s;", (
				False, id_state
			))

		return {
			'message': 'state successfully removed'
		}