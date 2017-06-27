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

	def get(self, type=None):
		""" Return all information for unit of measure

		:param type: STRING
		"""
		with Database() as db:
			if type is None:
				data = db.query(Table).all()
			else:
				data = db.query(Table).filter(Table.type == type).all()

		return {
			'data': data
		}