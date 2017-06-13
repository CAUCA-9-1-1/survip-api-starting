from framework.manage.database import Database
from framework.resturls.base import Base
from ..models.risk_level import RiskLevel as Table


class RiskLevel(Base):
	table_name = 'tbl_risk_level'
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_risk_level=None, is_active=None):
		""" Return all information for risk level

		:param id_risk_level: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_risk_level is None and is_active is None:
				data = db.query(Table).all()
			elif id_risk_level is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_risk_level)

		return {
			'data': data
		}
