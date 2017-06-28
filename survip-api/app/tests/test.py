import unittest
from ..resturls.test import Test


class TestTest(unittest.TestCase):
	def setUp(self):
		pass

	def test_01_get(self):
		result = Test().get()

		self.assertEqual(result['method test'], "GET")

	def test_02_modify(self):
		result = Test().modify()

		self.assertEqual(result['method test'], "PUT")