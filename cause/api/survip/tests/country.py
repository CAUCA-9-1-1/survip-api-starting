import unittest
from cause.api.management.core.manage.database import Database
from ..resturls.country import Country


class TestCountry(unittest.TestCase):
	def setUp(self):
		self.id_country = None

	def test_01_insert(self):
		result = Country().create({
			'name': 'country for unittest',
			'code_alpha2': 'XX'
		})

		self.__class__.id_country = result['id_country']
		self.assertEqual(result['message'], "country successfully created")

	def test_02_get(self):
		result = Country().get(self.__class__.id_country)
		self.assertEqual(result['data'].code_alpha2, 'XX')

	def test_03_modify(self):
		result = Country().modify({
			'id_country': self.__class__.id_country,
			'code_alpha2': 'VV'
		})

		self.assertEqual(result['message'], "country successfully modified")

	def test_04_get(self):
		result = Country().get(self.__class__.id_country)
		self.assertEqual(result['data'].code_alpha2, 'VV')

	def test_05_remove(self):
		result = Country().remove(self.__class__.id_country)
		self.assertEqual(result['message'], "country successfully removed")

	def test_06_delete(self):
		with Database() as db:
			db.execute("DELETE FROM tbl_country WHERE id_country::UUID='%s';" % self.__class__.id_country)