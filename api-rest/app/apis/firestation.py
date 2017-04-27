from causeweb.storage.db import DB
from causeweb.apis.base import Base


class Firestation(Base):
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_firestation):
		""" Return all information for one firestation

		:param id_firestation: UUID
		"""
		with DB() as db:
			data = db.get_row("""SELECT * FROM tbl_firestation
                                WHERE id_firestation=%s;""", (id_firestation,))

		return {
			'data': data
		}