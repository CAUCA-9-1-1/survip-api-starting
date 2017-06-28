import unittest
from cause.api.management.core.manage.database import Database
from ..resturls.region import Region


class TestRegion(unittest.TestCase):
	def setUp(self):
		self.id_region = None

	def test_01_insert(self):
		result = Region().create({
			'name': 'region for unittest',
			'id_state': 'cf6b91c3-08ac-4d06-b5ed-9396c99f2c18'
		})

		self.__class__.id_region = result['id_region']
		self.assertEqual(result['message'], "region successfully created")

	def test_02_get(self):
		result = Region().get(self.__class__.id_region)
		self.assertEqual(result['data'].name['fr'], 'region for unittest')

	def test_03_modify(self):
		result = Region().modify({
			'id_region': self.__class__.id_region,
			'name': 'region for unittest+modify'
		})

		self.assertEqual(result['message'], "region successfully modified")

	def test_04_get(self):
		result = Region().get(self.__class__.id_region)
		self.assertEqual(result['data'].name['fr'], 'region for unittest+modify')

	def test_05_remove(self):
		result = Region().remove(self.__class__.id_region)
		self.assertEqual(result['message'], "region successfully removed")

	def test_06_delete(self):
		with Database() as db:
			db.execute("DELETE FROM tbl_region WHERE id_region::UUID='%s';" % self.__class__.id_region)