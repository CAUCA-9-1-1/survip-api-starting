import unittest
from .building import TestBuilding
from .city import TestCity
from .inspection import TestInspection


def get_test_opensource(suite=None):
	if suite is None:
		suite = unittest.TestSuite()

	suite.addTest(unittest.makeSuite(TestBuilding))
	suite.addTest(unittest.makeSuite(TestCity))
	suite.addTest(unittest.makeSuite(TestInspection))

	return suite