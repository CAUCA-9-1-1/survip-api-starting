from framework.manage.database import Database
from framework.resturls.base import Base
from ..models.construction_type import ConstructionType as Table


class ConstructionType(Base):
	table_name = 'tbl_construction_type'
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_construction_type=None, is_active=None):
		""" Return all information for construction type

		:param id_construction_type: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_construction_type is None and is_active is None:
				data = db.query(Table).all()
			elif id_construction_type is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_construction_type)

		return {
			'data': data
		}