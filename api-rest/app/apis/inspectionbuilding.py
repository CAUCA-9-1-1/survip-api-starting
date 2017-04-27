from causeweb.storage.db import DB
from causeweb.apis.base import Base


class InspectionBuilding(Base):
	mapping_method = {
		'GET': '',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get_last(self, id_building):
		""" Return last inspection of one building

		:param id_building: UUID
		"""
		with DB() as db:
			return db.get("""SELECT created_on
								FROM tbl_inspection
								WHERE id_building=%s AND is_completed=%s
								ORDER BY created_on;""", (id_building, True))

		return None
