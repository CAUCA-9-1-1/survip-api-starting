import unittest
from ..app.resturls.building import Building


class TestBuilding(unittest.TestCase):
	def setUp(self):
		self.id_building = None

	def test_00_insert(self):
		result = Building().create({
			'name': 'building pour unittest',
			'civic_number': '1234'
		})

		self.__class__.id_building = result['id_building']
		self.assertEqual(result['message'], "building successfully created")

	def test_01_get(self):
		result = Building().get(self.__class__.id_building)
		self.assertEqual(result['data'].civic_number, '1234')

	def test_02_modify(self):
		result = Building().modify({
			'id_building': self.__class__.id_building,
			'civic_number': '2345'
		})

		self.assertEqual(result['message'], "building successfully modified")

	def test_03_get(self):
		result = Building().get(self.__class__.id_building)
		self.assertEqual(result['data'].civic_number, '2345')

	def test_04_remove(self):
		result = Building().remove(self.__class__.id_building)
		self.assertEqual(result['message'], "building successfully removed")
