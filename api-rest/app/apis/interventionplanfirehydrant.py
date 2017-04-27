from causeweb.storage.db import DB
from causeweb.apis.base import Base
from .firehydrant import FireHydrant


class InterventionPlanFireHydrant(Base):
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_intervention_plan):
		""" Return all fire hydrant for intervention plan

		:param id_intervention_plan: UUID
		"""
		with DB() as db:
			data = db.get_all("""SELECT * FROM tbl_intervention_plan_fire_hydrant
                                WHERE id_intervention_plan=%s;""", (id_intervention_plan,))

		for key, row in enumerate(data):
			data[key].update({
				'fire_hydrant': FireHydrant().get(row['id_fire_hydrant'])['data']
			})

		return {
			'data': data
		}