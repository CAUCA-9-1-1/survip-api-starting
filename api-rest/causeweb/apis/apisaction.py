from ..storage.db import DB
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
		with DB() as db:
			data = db.get_all("""SELECT tbl_apis_action.*, CONCAT(attr1.attribute_value, ' ', attr2.attribute_value) AS user FROM tbl_apis_action
								LEFT JOIN tbl_webuser wu ON wu.id_webuser=tbl_apis_action.id_webuser
								LEFT JOIN tbl_webuser_attributes attr1 ON attr1.id_webuser = wu.id_webuser AND attr1.attribute_name='first_name'
								LEFT JOIN tbl_webuser_attributes attr2 ON attr2.id_webuser = wu.id_webuser AND attr2.attribute_name='last_name';""")

		return {
			'data': data
		}
