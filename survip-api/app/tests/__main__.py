import unittest
from .test import TestTest


def get_test_app(suite=None):
	if suite is None:
		suite = unittest.TestSuite()

	suite.addTest(unittest.makeSuite(TestTest))

	return suite