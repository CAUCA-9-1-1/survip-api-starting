from causeweb.storage.db import DB
from causeweb.apis.base import Base
from .constructiontype import ConstructionType


class InterventionPlanStructure(Base):
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_intervention_plan):
		""" Return all fire hydrant for intervention plan

		:param id_intervention_plan: UUID
		"""
		with DB() as db:
			data = db.get_row("""SELECT * FROM tbl_intervention_plan_structure
                                WHERE id_intervention_plan=%s;""", (id_intervention_plan,))

		data.update({
			'construction_type': ConstructionType().get(data['id_construction_type'])['data'],
			'construction_type_for_joits': ConstructionType().get(data['id_construction_type_for_joits'])['data']
		})

		return {
			'data': data
		}

	def modify(self, args):
		""" Modify all information for intervention plan structure

		:param args: {
			id_intervention_plan: UUID,
			sprinkler_type: STRING,
			sprinkler_floor: STRING,
			sprinkler_wall: STRING,
			sprinkler_sector: STRING,
		}
		"""
		with DB() as db:
			db.execute("""UPDATE tbl_intervention_plan_structure SET
							sprinkler_type=%s, sprinkler_floor=%s, sprinkler_wall=%s, sprinkler_sector=%s
						  WHERE id_intervention_plan=%s;""", (
				args['sprinkler_type'], args['sprinkler_floor'], args['sprinkler_wall'], args['sprinkler_sector']
			))

		return {
			'message': 'intervention plan structure successfully modified'
		}