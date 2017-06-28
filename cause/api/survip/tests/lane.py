import unittest

from api.management.core.database import Database
from ..resturls.lane import Lane


class TestLane(unittest.TestCase):
	def setUp(self):
		self.id_lane = None

	def test_01_insert(self):
		result = Lane().create({
			'name': 'lane for unittest',
			'id_city': 'c5994214-ce5b-4b40-b95e-1b04491b0ede'
		})

		self.__class__.id_lane = result['id_lane']
		self.assertEqual(result['message'], "lane successfully created")

	def test_02_get(self):
		result = Lane().get(self.__class__.id_lane)
		self.assertEqual(result['data'].name['fr'], 'lane for unittest')

	def test_03_modify(self):
		result = Lane().modify({
			'id_lane': self.__class__.id_lane,
			'name': 'lane for unittest+modify'
		})

		self.assertEqual(result['message'], "lane successfully modified")

	def test_04_get(self):
		result = Lane().get(self.__class__.id_lane)
		self.assertEqual(result['data'].name['fr'], 'lane for unittest+modify')

	def test_05_remove(self):
		result = Lane().remove(self.__class__.id_lane)
		self.assertEqual(result['message'], "lane successfully removed")

	def test_06_delete(self):
		with Database() as db:
			db.execute("DELETE FROM tbl_lane WHERE id_lane::UUID='%s';" % self.__class__.id_lane)