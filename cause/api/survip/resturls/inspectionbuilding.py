from api.management.core.database import Database
from cause.api.management.resturls.base import Base
from ..models.fire_safety_department_city_serving import FireSafetyDepartmentCityServing
from ..models.inspection_building import InspectionBuilding as Table
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
			data = db.query(Table).join(
				Lane, Lane.id_lane == Table.id_lane
			).join(
				FireSafetyDepartmentCityServing, FireSafetyDepartmentCityServing.id_city == Lane.id_city
			).join(
				WebuserFireSafetyDepartment, WebuserFireSafetyDepartment.id_fire_safety_department == FireSafetyDepartmentCityServing.id_fire_safety_department
			).filter(
				Table.is_active == True,
				WebuserFireSafetyDepartment.id_webuser == Base.logged_id_webuser
			).all()

		return {
			'data': data
		}
