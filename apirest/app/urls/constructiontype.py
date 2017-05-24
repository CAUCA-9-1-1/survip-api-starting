from causeweb.storage.db import DB
from causeweb.apis.base import Base


class ConstructionType(Base):
	table_name = 'tbl_construction_type'
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_construction_type):
		""" Return all information for one construction type

		:param id_construction_type: UUID
		"""
		with DB() as db:
			data = db.get_row("""SELECT * FROM tbl_construction_type
                                WHERE id_construction_type=%s;""", (id_construction_type,))

		return {
			'data': data
		}