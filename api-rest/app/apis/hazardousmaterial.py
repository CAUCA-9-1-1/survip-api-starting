from causeweb.storage.db import DB
from causeweb.session.general import Session
from causeweb.apis.base import Base


class HazardousMaterial(Base):
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_hazardous_material=None):
		""" Return all information for hazardous material

		:param id_hazardous_material: UUID
		"""
		with DB() as db:
			if id_hazardous_material is None:
				data = db.get_all("""SELECT * FROM tbl_hazardous_material WHERE id_hazardous_material=%s AND is_active=%s""", (Session.get('userId'), True))
			else:
				data = db.get_all("""SELECT * FROM tbl_hazardous_material
	                                WHERE id_hazardous_material=%s;""", (id_hazardous_material))

		return {
			'data': data
		}