from causeweb.storage.db import DB
from causeweb.apis.base import Base
from causeweb.site.multilang import MultiLang
from causeweb.session.general import Session
from .lane import Lane
from .risklevel import RiskLevel
from .inspectionbuilding import InspectionBuilding


class Building(Base):
	table_name = 'tbl_building'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_building=None):
		""" Return all building information

		:param id_building: UUID or STRING
		"""
		with DB() as db:
			if id_building == 'forinspection':
				if self.has_permission('RightTPI') is False:
					return self.no_access()

				data = db.get_all("""SELECT id_building, tbl_building.id_language_content_name, id_risk_level, civic_number, civic_letter, tbl_building.id_lane, matricule
									FROM tbl_building
									LEFT JOIN tbl_lane ON tbl_lane.id_lane = tbl_building.id_lane
									LEFT JOIN tbl_fire_safety_department_city_serving ON tbl_fire_safety_department_city_serving.id_city = tbl_lane.id_city
									LEFT JOIN tbl_webuser_fire_safety_department ON tbl_webuser_fire_safety_department.id_fire_safety_department = tbl_fire_safety_department_city_serving.id_fire_safety_department
									WHERE
										tbl_building.is_active=True AND
										tbl_webuser_fire_safety_department.id_webuser = %s;""", (Session.get('userID'),))
			elif id_building is None:
				if self.has_permission('RightAdmin') is False:
					return self.no_access()

				data = db.get_all("SELECT * FROM tbl_building;")
			elif id_building != 'forinspection':
				data = db.get_all("SELECT * FROM tbl_building WHERE id_building=%s;", (id_building,))

		for key, row in enumerate(data):
			data[key]['name'] = MultiLang.get(row['id_language_content_name'])
			data[key]['lane'] = Lane().get(row['id_lane'])
			data[key]['risk_level'] = RiskLevel().get(row['id_risk_level'])
			data[key]['last_inspection'] = InspectionBuilding().get_last(row['id_building'])

		return {
			'data': data
		} if id_building is None or id_building == 'forinspection' else data[0]

	def modify(self, args):
		""" Modify all information for building

		:param args: {
			id_building: UUID,
			name: JSON
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		id_language_content = MultiLang.set(args['name'])

		with DB() as db:
			db.execute("""UPDATE tbl_building SET
							id_language_content_name=%s, year_of_construction=%s, building_value=%s, number_of_floors=%s, number_of_appartment=%s
						  WHERE id_building=%s;""", (
				id_language_content, args['year_of_construction'], args['building_value'], args['number_of_floors'], args['number_of_appartment'],
				args['id_building']
			))

		return {
			'message': 'building successfully modified'
		}