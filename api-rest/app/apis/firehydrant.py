from causeweb.storage.db import DB
from causeweb.apis.base import Base


class FireHydrant(Base):
	table_name = 'tbl_fire_hydrant'
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_fire_hydrant):
		""" Return all information for one fire hydrant

		:param id_fire_hydrant: UUID
		"""
		with DB() as db:
			data = db.get_row("""SELECT * FROM tbl_fire_hydrant
                                WHERE id_fire_hydrant=%s;""", (id_fire_hydrant,))

		return {
			'data': data
		}