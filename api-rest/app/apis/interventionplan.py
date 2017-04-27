from causeweb.storage.db import DB
from causeweb.apis.base import Base
from .city import City
from .firestation import Firestation


class InterventionPlan(Base):
	table_name = 'tbl_intervention_plan'
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': 'modify',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_intervention_plan):
		""" Return all information for intervention plan

		:param id_intervention_plan: UUID
		"""
		with DB() as db:
			data = db.get_row("""SELECT * FROM tbl_intervention_plan
                                WHERE id_intervention_plan=%s;""", (id_intervention_plan,))

		data['city'] = City().get(data['id_city'])['data']
		data['firestation_course1'] = Firestation().get(data['id_firestation_course1'])['data']
		data['firestation_course2'] = Firestation().get(data['id_firestation_course2'])['data']
		data['firestation_course3'] = Firestation().get(data['id_firestation_course3'])['data']

		return {
			'data': data
		}

	def modify(self, args):
		""" Modify all information for intervention plan

		:param args: {
			id_intervention_plan: UUID,
			plan_course1: STRING,
			id_firestation_course1: UUID,
			other_information: STRING,
		}
		"""
		with DB() as db:
			db.execute("""UPDATE tbl_intervention_plan SET
							plan_course1=%s, id_firestation_course1=%s, other_information=%s
						  WHERE id_intervention_plan=%s;""", (
				args['plan_course1'], args['id_firestation_course1'], args['other_information']
			))

		return {
			'message': 'intervention plan successfully modified'
		}