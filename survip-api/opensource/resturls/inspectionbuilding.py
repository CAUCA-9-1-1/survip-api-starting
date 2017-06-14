from framework.manage.database import Database
from framework.resturls.base import Base
from ..models.building import Building
from ..models.fire_safety_department_city_serving import FireSafetyDepartmentCityServing
from ..models.inspection import Inspection
from ..models.lane import Lane
from ..models.webuser_fire_safety_department import WebuserFireSafetyDepartment


class InspectionBuilding(Base):
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self):
		if self.has_permission('RightTPI') is False:
			return self.no_access()

		with Database() as db:
			data = db.query(Building).join(
				Lane, Lane.id_lane == Building.id_lane
			).join(
				FireSafetyDepartmentCityServing, FireSafetyDepartmentCityServing.id_city == Lane.id_city
			).join(
				WebuserFireSafetyDepartment, WebuserFireSafetyDepartment.id_fire_safety_department == FireSafetyDepartmentCityServing.id_fire_safety_department
			).join(
				Inspection, Inspection.id_building == Building.id_building
			).filter(
				Building.is_active == True,
				WebuserFireSafetyDepartment.id_webuser == Base.logged_id_webuser
			).all()

		return {
			'data': data
		}
