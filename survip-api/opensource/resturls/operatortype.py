from framework.manage.database import Database
from framework.resturls.base import Base
from ..models.operator_type import OperatorType as Table


class OperatorType(Base):
	table_name = 'tbl_operator_type'
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_operator_type=None, is_active=None):
		""" Return all information for operator type

		:param id_operator_type: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_operator_type is None and is_active is None:
				data = db.query(Table).all()
			elif id_operator_type is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_operator_type)

		return {
			'data': data
		}