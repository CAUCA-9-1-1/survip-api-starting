from framework.manage.database import Database
from framework.resturls.base import Base
from ..models.utilisation_code import UtilisationCode as Table


class UtilisationCode(Base):
	table_name = 'tbl_utilisation_code'
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_utilisation_code=None, is_active=None):
		""" Return all information for utilisation code

		:param id_utilisation_code: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_utilisation_code is None and is_active is None:
				data = db.query(Table).all()
			elif id_utilisation_code is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_utilisation_code)

		return {
			'data': data
		}
