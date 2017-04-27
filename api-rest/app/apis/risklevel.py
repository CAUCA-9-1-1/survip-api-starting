from causeweb.storage.db import DB
from causeweb.site.multilang import MultiLang
from causeweb.apis.base import Base


class RiskLevel(Base):
	table_name = 'tbl_risk_level'
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_risk_level):
		""" Return all information for one risk level

		:param id_risk_level: UUID
		"""
		with DB() as db:
			data = db.get_all("""SELECT code, id_language_content_name, color FROM tbl_risk_level
                                WHERE id_risk_level=%s;""", (id_risk_level,))

		for key, row in enumerate(data):
			data[key]['name'] = MultiLang.get(row['id_language_content_name'])

		return {
			'data': data
		} if id_risk_level is None else data[0]