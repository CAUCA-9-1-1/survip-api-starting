from framework.manage.database import Database
from framework.resturls.base import Base
from ..models.fire_hydrant_type import FireHydrantType as Table


class FireHydrantType(Base):
	table_name = 'tbl_fire_hydrant_type'
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_fire_hydrant_type=None, is_active=None):
		""" Return all information for fire hydrant type

		:param id_fire_hydrant_type: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_fire_hydrant_type is None and is_active is None:
				data = db.query(Table).all()
			elif id_fire_hydrant_type is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_fire_hydrant_type)

		return {
			'data': data
		}