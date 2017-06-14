from framework.manage.database import Database
from framework.resturls.base import Base
from ..models.construction_type import ConstructionType as Table


class FireHydrant(Base):
	table_name = 'tbl_fire_hydrant'
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_fire_hydrant=None, is_active=None):
		""" Return all information for fire hydrant

		:param id_fire_hydrant: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_fire_hydrant is None and is_active is None:
				data = db.query(Table).all()
			elif id_fire_hydrant is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_fire_hydrant)

		return {
			'data': data
		}