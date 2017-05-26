import unittest
from framework.manage.database import Database
from opensource.resturls.building import Building


class TestBuilding(unittest.TestCase):
	def setUp(self):
		self.id_building = None

	def test_01_insert(self):
		result = Building().create({
			'name': 'building pour unittest',
			'civic_number': '1234'
		})

		self.__class__.id_building = result['id_building']
		self.assertEqual(result['message'], "building successfully created")

	def test_02_get(self):
		result = Building().get(self.__class__.id_building)
		self.assertEqual(result['data'].civic_number, '1234')

	def test_03_modify(self):
		result = Building().modify({
			'id_building': self.__class__.id_building,
			'civic_number': '2345'
		})

		self.assertEqual(result['message'], "building successfully modified")

	def test_04_get(self):
		result = Building().get(self.__class__.id_building)
		self.assertEqual(result['data'].civic_number, '2345')

	def test_05_remove(self):
		result = Building().remove(self.__class__.id_building)
		self.assertEqual(result['message'], "building successfully removed")

	def test_06_delete(self):
		with Database() as db:
			db.execute("DELETE FROM tbl_building WHERE id_building::UUID='%s';" % self.__class__.id_building)