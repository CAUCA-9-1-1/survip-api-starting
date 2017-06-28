import unittest

from api.management.core.database import Database
from ..resturls.county import County


class TestCounty(unittest.TestCase):
	def setUp(self):
		self.id_county = None

	def test_01_insert(self):
		result = County().create({
			'name': 'county for unittest',
			'id_state': 'cf6b91c3-08ac-4d06-b5ed-9396c99f2c18'
		})

		self.__class__.id_county = result['id_county']
		self.assertEqual(result['message'], "county successfully created")

	def test_02_get(self):
		result = County().get(self.__class__.id_county)
		self.assertEqual(result['data'].name['fr'], 'county for unittest')

	def test_03_modify(self):
		result = County().modify({
			'id_county': self.__class__.id_county,
			'name': 'county for unittest+modify'
		})

		self.assertEqual(result['message'], "county successfully modified")

	def test_04_get(self):
		result = County().get(self.__class__.id_county)
		self.assertEqual(result['data'].name['fr'], 'county for unittest+modify')

	def test_05_remove(self):
		result = County().remove(self.__class__.id_county)
		self.assertEqual(result['message'], "county successfully removed")

	def test_06_delete(self):
		with Database() as db:
			db.execute("DELETE FROM tbl_county WHERE id_county::UUID='%s';" % self.__class__.id_county)