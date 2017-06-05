from datetime import date, timedelta
from ..manage.database import Database
from .base import Base


class WebuserStatistic(Base):
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, type, period_start=None, period_end=None):
		""" Return all user statistics

		:param type: type of data
		:param period_start: TIMESTAMP
		:param period_end: TIMESTAMP
		"""
		if period_start is None:
			period_end = date.today()
			period_start = period_end - timedelta(days=30)

		if type == 'connectionByDate':
			return {
				'data': self.connection_by_date(period_start, period_end)
			}
		elif type == 'requestByTable':
			return {
				'data': self.request_by_table(period_start, period_end)
			}

		return {
			'error': 'Unknown type of data "%s"' % type
		}

	def connection_by_date(self, period_start, period_end):
		with Database() as db:
			return db.execute("""SELECT count(token.created_on) AS total, to_char(token.created_on, 'YYYY/MM/DD') AS days
								FROM tbl_access_token token
								WHERE token.created_on>=%s AND token.created_on<%s
								GROUP BY days;""", (period_start, period_end))

	def request_by_table(self, period_start, period_end):
		with Database() as db:
			return db.execute("""SELECT count(action_time) AS total, action_object AS table
								FROM tbl_apis_action aa
						        WHERE aa.action_time>=%s AND aa.action_time<%s
						        GROUP BY action_object;""", (period_start, period_end))
