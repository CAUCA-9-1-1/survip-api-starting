from sqlalchemy.orm import joinedload, subqueryload

from framework.manage.database import Database
from framework.resturls.base import Base
from opensource.models.datatransfertobjects.BuildingForDisplay import BuildingForDisplay as Building
from opensource.models.intervention_plan import InterventionPlan as Plan
from opensource.models.intervention_plan_building import InterventionPlanBuilding as PlanBuilding
from opensource.models.lane import Lane
from opensource.resturls.mappers.building_for_display_loader import BuildingForDisplayLoader


class InterventionPlanGeneralInformations(Base):
	table_name = 'tbl_intervention_plan'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, language, id_intervention_plan):
		""" Return all information for intervention plan

		:param id_intervention_plan: UUID
		"""
		with Database() as db:
			plan = db.query(Plan).\
				filter(Plan.is_active == '1', Plan.id_intervention_plan == id_intervention_plan).\
				first()
			data = {'plan': plan, 'planBuilding': None, 'building': None}

			if plan is not None:
				planbuilding = db.query(PlanBuilding).\
					filter(PlanBuilding.is_active == '1',
						   PlanBuilding.id_intervention_plan == id_intervention_plan,
						   PlanBuilding.is_parent == '1').\
					first()
				data = {'plan': plan, 'planBuilding': planbuilding, 'building': None}

				if planbuilding is not None:
					building = db.query(Building). \
						filter(Building.is_active == '1', Building.id_building == planbuilding.id_building). \
						first()
					if building is not None:
						BuildingForDisplayLoader.set_address_description(language, building)
					data = {'plan': plan, 'planBuilding': planbuilding, 'building': building}

		return {'data': data}