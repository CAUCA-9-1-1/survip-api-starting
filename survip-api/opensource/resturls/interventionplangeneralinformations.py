from framework.manage.database import Database
from framework.resturls.base import Base
from ..models.interventionplan import InterventionPlan as Table


class InterventionPlanGeneralInformations(Base):
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
		with Database() as db:
			data = db.query(Table).filter(Table.is_active == '1', Table.id_intervention_plan == id_intervention_plan).all()

		return {'data': data}