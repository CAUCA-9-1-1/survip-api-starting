from datetime import date, timedelta
from framework.manage.database import Database
from framework.resturls.base import Base


class InspectionStatistic(Base):
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, period_start, period_end):
		""" Return all inspection statistics

		:param period_start: TIMESTAMP
		:param period_end: TIMESTAMP
		"""
		if self.has_permission('RightTPI') is False:
			return self.no_access()

		if period_start is None:
			period_end = date.today()
			period_start = period_end - timedelta(days=30)

		return {
			'data': self.get_by_date(period_start, period_end)
		}

	def get_by_date(self, period_start, period_end):
		with Database() as db:
			return db.execute("""SELECT count(answered_on) AS total, to_char(ia.answered_on, 'YYYY/MM/DD') AS days
								FROM tbl_inspection_answer ia
								WHERE ia.answered_on>=%s AND ia.answered_on<%s
								GROUP BY days;""", (period_start, period_end))
