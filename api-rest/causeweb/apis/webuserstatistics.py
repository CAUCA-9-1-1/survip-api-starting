from .base import Base
from ..storage.db import DB


class WebuserStatistics(Base):
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, period_start, period_end):
		""" Return all user statistics

		:param period_start: TIMESTAMP
		:param period_end: TIMESTAMP
		"""
		return {
			'by_date': self.get_by_date(period_start, period_end),
			'by_apps': self.get_by_application(period_start, period_end),
			'by_page': self.get_by_page(period_start, period_end),
			'by_platform': self.get_by_platform(period_start, period_end)
		}

	def get_by_date(self, period_start, period_end):
		with DB() as db:
			return db.get_all("""SELECT count(action_time) AS total, to_char(wa.action_time, 'YYYY/MM/DD') AS days
								FROM tbl_webuser_action wa
								WHERE wa.action_name='logon' AND wa.action_time>=%s AND wa.action_time<%s
								GROUP BY days;""", (period_start, period_end))

	def get_by_application(self, period_start, period_end):
		with DB() as db:
			return db.get_all("""SELECT count(action_time) AS total, SUBSTRING(
						            wa.action_param,
						            position('application' in wa.action_param) + 15,
						            position('"' in SUBSTRING(wa.action_param, position('application' in wa.action_param) + 15)) - 1
						        ) AS apps
								FROM tbl_webuser_action wa
						        WHERE wa.action_name='logon' AND wa.action_time>=%s AND wa.action_time<%s
						        GROUP BY apps;""", (period_start, period_end))

	def get_by_page(self, period_start, period_end):
		with DB() as db:
			return db.get_all("""SELECT count(action_time) AS total, SUBSTRING(action_object, 11) AS page
								FROM tbl_webuser_action wa
						        WHERE wa.action_name='loadpage' AND wa.action_time>=%s AND wa.action_time<%s
						        GROUP BY action_object;""", (period_start, period_end))

	def get_by_platform(self, period_start, period_end):
		with DB() as db:
			return db.get_all("""SELECT count(action_time) AS total, SUBSTRING(
						            wa.action_param,
						            position('platform' in wa.action_param) + 12,
						            position('"' in SUBSTRING(wa.action_param, position('platform' in wa.action_param) + 12)) - 1
						        ) AS platform
								FROM tbl_webuser_action wa
						        WHERE wa.action_name='logon' AND wa.action_time>=%s AND wa.action_time<%s
						        GROUP BY platform;""", (period_start, period_end))