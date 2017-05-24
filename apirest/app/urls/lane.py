import uuid
from causeweb.storage.db import DB
from causeweb.site.multilang import MultiLang
from causeweb.apis.base import Base
from .city import City


class Lane(Base):
	table_name = 'tbl_lane'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_lane=None, is_active=None):
		""" Return all lane information

		:param id_lane: UUID
		"""
		with DB() as db:
			if id_lane is None and is_active is None:
				data = db.get_all("SELECT * FROM tbl_lane;")
			elif id_lane is None:
				data = db.get_all("SELECT * FROM tbl_lane WHERE is_active=%s;", (is_active,))
			else:
				data = db.get_all("SELECT * FROM tbl_lane WHERE id_lane=%s;", (id_lane,))

		for key, row in enumerate(data):
			data[key]['name'] = MultiLang.get(row['id_language_content_name'])
			data[key]['city'] = City().get(row['id_city'])

		return {
			'data': data
		} if id_lane is None else data[0]

	def create(self, args):
		""" Create a new lane

		:param args: {
			name: JSON,
			id_city: UUID
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		id_lane = uuid.uuid4()
		id_language_content = MultiLang.set(args['name'], True)

		with DB() as db:
			db.execute("""INSERT INTO tbl_lane(
							id_lane, id_language_content_name, id_city, is_active
						  ) VALUES (%s, %s, %s, True);""", (
				id_lane, id_language_content, args['id_city']
			))

		return {
			'id_lane': id_lane,
			'message': 'lane successfully created'
		}

	def modify(self, args):
		""" Modify a lane

		:param args: {
			id_lane: UUID,
			name: JSON,
			id_city: UUID,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'id_lane' not in args:
			raise Exception("You need to pass a id_lane")

		id_language_content = MultiLang.set(args['name'])

		with DB() as db:
			db.execute("""UPDATE tbl_lane SET
			           	id_language_content_name=%s, id_city=%s, is_active=%s
			           WHERE id_city=%s;""", (
				id_language_content, args['id_city'], args['is_active'], args['id_lane']
			))

		return {
			'message': 'lane successfully modify'
		}

	def remove(self, id_lane):
		""" Remove a lane

		:param id_lane: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with DB() as db:
			db.execute("UPDATE tbl_lane SET is_active=%s WHERE id_lane=%s;", (
				False, id_lane
			))

		return {
			'message': 'lane successfully removed'
		}