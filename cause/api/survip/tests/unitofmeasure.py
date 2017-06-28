import unittest
from ..resturls.unitofmeasure import UnitOfMeasure


class TestUnitOfMeasure(unittest.TestCase):
	def setUp(self):
		pass

	def test_01_get(self):
		result = UnitOfMeasure().get()
		isList = isinstance(result['data'], list)

		self.assertEqual(isList, True)
