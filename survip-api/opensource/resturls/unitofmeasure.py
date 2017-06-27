from framework.manage.database import Database
from framework.resturls.base import Base
from ..models.unit_of_measure import UnitOfMeasure as Table


class UnitOfMeasure(Base):
	table_name = 'tbl_unit_of_measure'
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_unit_of_measure=None, is_active=None):
		""" Return all information for unit of measure

		:param id_unit_of_measure: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_unit_of_measure is None and is_active is None:
				data = db.query(Table).all()
			elif id_unit_of_measure is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_unit_of_measure)

		return {
			'data': data
		}