from causepy.manage.database import Database
from causepy.resturls.base import Base
from ..models.inspection import Inspection as Table
from ..models.building import Building
from ..models.lane import Lane


class InspectionByUser(Base):
	table_name = 'tbl_inspection'
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_city=None):
		""" Return all inspection for the connected user

		:param id_city: UUID
		"""
		with Database() as db:
			if id_city is None:
				data = db.query(Table).filter(
					Table.is_active == True,
					Table.is_completed == False
				).all()
			else:
				data = db.query(Table).join(
					Building, Table.id_building == Building.id_building
				).join(
					Lane, Building.id_lane == Lane.id_lane
				).filter(
					Table.is_active == True,
					Table.is_completed == False,
					Lane.id_city == id_city
				).all()

		return {
			'data': data
		}
