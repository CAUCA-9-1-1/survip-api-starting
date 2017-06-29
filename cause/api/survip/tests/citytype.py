import unittest
from cause.api.management.core.database import Database
from ..resturls.citytype import CityType


class TestCityType(unittest.TestCase):
	def setUp(self):
		self.id_city_type = None

	def test_01_insert(self):
		result = CityType().create({
			'name': 'city type for unittest'
		})

		self.__class__.id_city_type = result['id_city_type']
		self.assertEqual(result['message'], "city type successfully created")

	def test_02_get(self):
		result = CityType().get(self.__class__.id_city_type)
		self.assertEqual(result['data'].name['fr'], 'city type for unittest')

	def test_03_modify(self):
		result = CityType().modify({
			'id_city_type': self.__class__.id_city_type,
			'name': 'city type for unittest+modify'
		})

		self.assertEqual(result['message'], "city type successfully modified")

	def test_04_get(self):
		result = CityType().get(self.__class__.id_city_type)
		self.assertEqual(result['data'].name['fr'], 'city type for unittest+modify')

	def test_05_remove(self):
		result = CityType().remove(self.__class__.id_city_type)
		self.assertEqual(result['message'], "city type successfully removed")

	def test_06_delete(self):
		with Database() as db:
			db.execute("DELETE FROM tbl_city_type WHERE id_city_type::UUID='%s';" % self.__class__.id_city_type)