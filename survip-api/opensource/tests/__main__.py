import unittest
from .building import TestBuilding
from .city import TestCity
from .citytype import TestCityType
from .country import TestCountry
from .county import TestCounty
from .inspection import TestInspection


def get_test_opensource(suite=None):
	if suite is None:
		suite = unittest.TestSuite()

	suite.addTest(unittest.makeSuite(TestBuilding))
	suite.addTest(unittest.makeSuite(TestCity))
	suite.addTest(unittest.makeSuite(TestCityType))
	suite.addTest(unittest.makeSuite(TestCountry))
	suite.addTest(unittest.makeSuite(TestCounty))
	suite.addTest(unittest.makeSuite(TestInspection))

	return suite