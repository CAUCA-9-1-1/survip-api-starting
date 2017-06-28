import unittest
from cause.api.management.core.manage.database import Database
from ..resturls.city import City


class TestCity(unittest.TestCase):
	def setUp(self):
		self.id_city = None

	def test_01_insert(self):
		result = City().create({
			'name': 'city for unittest',
			'id_county': '511993cc-bcee-4a0e-bac9-4774109f3b62',
			'code': '12345'
		})

		self.__class__.id_city = result['id_city']
		self.assertEqual(result['message'], "city successfully created")

	def test_02_get(self):
		result = City().get(self.__class__.id_city)
		self.assertEqual(result['data'].code, '12345')

	def test_03_modify(self):
		result = City().modify({
			'id_city': self.__class__.id_city,
			'code': '23456'
		})

		self.assertEqual(result['message'], "city successfully modified")

	def test_04_get(self):
		result = City().get(self.__class__.id_city)
		self.assertEqual(result['data'].code, '23456')

	def test_05_remove(self):
		result = City().remove(self.__class__.id_city)
		self.assertEqual(result['message'], "city successfully removed")

	def test_06_delete(self):
		with Database() as db:
			db.execute("DELETE FROM tbl_city WHERE id_city::UUID='%s';" % self.__class__.id_city)