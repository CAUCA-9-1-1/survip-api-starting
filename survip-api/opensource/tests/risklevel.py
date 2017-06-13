import unittest
from ..resturls.risklevel import RiskLevel


class TestRiskLevel(unittest.TestCase):
	def setUp(self):
		pass

	def test_01_get(self):
		result = RiskLevel().get()
		isList = isinstance(result['data'], list)

		self.assertEqual(isList, True)
