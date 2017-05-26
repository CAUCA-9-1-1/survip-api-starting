import pdfkit
from causeweb import config
from causeweb.storage.db import DB
from causeweb.apis.base import Base


class InspectionReport(Base):
	mapping_method = {
		'GET': 'pdf',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def pdf(self, id_inspection_answer):
		""" Generate and return url of PDF

		:param id_inspection_answer: UUID
		"""
		if self.has_permission('RightTPI') is False:
			return self.no_access()

		with DB() as db:
			data = db.get_row("""SELECT * FROM tbl_inspection_answer
								  LEFT JOIN tbl_inspection ON tbl_inspection.id_inspection = tbl_inspection_answer.id_inspection
		                          WHERE id_inspection_answer=%s;""", (id_inspection_answer,))

		html = ''

		pdfkit.from_string(html, '%s/data/pdfs/%s.pdf' % (config.ROOT, id_inspection_answer), {
			'encoding': 'UTF-8'
		})

		return {
			'url': '/downloads/%s.pdf' % id_inspection_answer
		}