from ..manage.database import Database
from ..models.apis_action import ApisAction as Table
from .base import Base


class ApisAction(Base):
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self):
		""" Return all apis action information
		"""
		with Database() as db:
			data = db.query(Table).all()

		return {
			'data': data
		}
