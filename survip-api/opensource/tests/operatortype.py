import unittest
from ..resturls.operatortype import OperatorType


class TestOperatorType(unittest.TestCase):
	def setUp(self):
		pass

	def test_01_get(self):
		result = OperatorType().get()
		isList = isinstance(result['data'], list)

		self.assertEqual(isList, True)
