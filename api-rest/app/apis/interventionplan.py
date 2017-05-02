from causeweb.storage.db import DB
from causeweb.apis.base import Base
from .city import City
from .firestation import Firestation


class InterventionPlan(Base):
	table_name = 'tbl_intervention_plan'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_intervention_plan):
		""" Return all information for intervention plan

		:param id_intervention_plan: UUID
		"""
		with DB() as db:
			data = db.get_all("""SELECT * FROM tbl_intervention_plan
                                WHERE id_intervention_plan=%s;""", (id_intervention_plan,))

		#for key, row in enumerate(data):
			#data[key]['city'] = City().get(row['id_city'])
			#data[key]['firestation_course1'] = Firestation().get(row['id_firestation_course1'])['data']
			#data[key]['firestation_course2'] = Firestation().get(row['id_firestation_course2'])['data']
			#data[key]['firestation_course3'] = Firestation().get(row['id_firestation_course3'])['data']

		return {
			'data': data
		} if id_intervention_plan is None else data[0]

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