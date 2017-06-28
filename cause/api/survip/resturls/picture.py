from api.management.core.database import Database
from cause.api.management.resturls.base import Base
from ..models.picture import Picture as Table


class Picture(Base):
	table_name = 'tbl_picture'
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_picture=None, is_active=None):
		""" Return all information for picture

		:param id_picture: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_picture is None and is_active is None:
				data = db.query(Table).all()
			elif id_picture is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_picture)

		return {
			'data': data
		}
